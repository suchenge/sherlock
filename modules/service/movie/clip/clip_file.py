import os
import re
import threading

from ffmpy import FFmpeg
from datetime import datetime

from modules.tools.common_methods.unity_tools import ffmpeg_execute_path

from modules.service.movie.video.video_file import VideoFile

from modules.service.movie.clip.time_line import TimeLine
from modules.service.movie.clip.overseer import Overseer


class ClipFile(VideoFile):
    def __init__(self, video: VideoFile):
        super().__init__(video.path)

        self.__is_usable__ = False
        self.__need_merge__ = False
        self.__need_delete__ = False
        self.__ffmpeg_path__ = ffmpeg_execute_path()
        self.__time_line_file_path__ = str(os.path.join(self.__parent__, self.__uid__ + '.txt'))
        self.__concat_file_path__ = f'{self.__path__}.merge.txt'
        self.__merge_file_path__ = str(os.path.join(self.__parent__, self.__uid__ + f'.merge.{self.__type__}'))

        self.__time_lines__ = self.__build_time_lines__()
        if self.__time_lines__ is not None and len(self.__time_lines__) > 0:
            self.__is_usable__ = True

    @property
    def is_usable(self):
        return self.__is_usable__

    @property
    def need_merge(self):
        return self.__need_merge__

    @property
    def need_delete(self):
        return self.__need_delete__

    def delete(self):
        os.remove(self.__time_line_file_path__)
        os.remove(self.path)

    def merge(self):
        if self.__is_usable__ and len(self.__time_lines__) > 0:
            merge_list = []

            for time_line in self.__time_lines__:
                if os.path.exists(time_line.output_path):
                    merge_list.append(f'file \'{time_line.output_path}\'')
                else:
                    print(f'{time_line.output_path} does not exist')

            if len(merge_list) > 0:
                with open(self.__concat_file_path__, 'w', encoding='utf') as merge_file:
                    for line in merge_list:
                        merge_file.write(f'{line}\r\n')

                try:
                    FFmpeg(
                        global_options=['-f', 'concat'],
                        inputs={self.__concat_file_path__: ['-safe', '0']},
                        outputs={self.__merge_file_path__: ['-c', 'copy']},
                        executable=self.__ffmpeg_path__
                    ).run()

                    os.remove(self.__concat_file_path__)

                    for blueprint in self.__time_lines__:
                        os.remove(blueprint.output_path)

                except Exception as error:
                    print(error)

    def __build_time_lines__(self):
        if os.path.exists(self.__time_line_file_path__):
            time_lines = []
            index = 0
            with open(self.__time_line_file_path__, 'r') as fs:
                while True:
                    line = fs.readline()

                    if not line:
                        break

                    line = line.strip()

                    if line == "merge":
                        self.__need_merge__ = True
                        continue

                    if line == "delete":
                        self.__need_delete__ = True
                        continue

                    lines = line.split(' ')
                    time = {
                        'start': self.__format_time___(lines[0]),
                        'end': self.__format_time___(lines[1]),
                    }
                    time_lines.append(TimeLine(self, index, time))
                    index += 1

            return time_lines

    def __build_time_line__(self, line_line: TimeLine):
        return line_line.output_name, line_line.output_path, line_line.start_time, line_line.end_time, line_line.length_time

    def __format_time___(self, time):
        result = time
        if '.' in time:
            result = result.replace('.', ':')

        match = re.compile(r'(\d{2})(\d{2})(\d{2})').findall(time)
        if match:
            result = ':'.join(match[0])

        return result.strip()

    def cut(self):
        if self.__is_usable__:
            current_timer = datetime.now()
            tasks = []

            for time_line in self.__time_lines__:
                tasks.append({
                                'time_line': self.__build_time_line__(time_line),
                                'status': 'waiting',
                                'start_time': current_timer,
                                'end_time': current_timer,
                                'executor': threading.Thread(target=self.__cut__, args=[time_line])
                             })

            overseer = Overseer(tasks)
            overseer.start()

            for task in tasks:
                task['executor'].start()
                task['status'] = 'running'
                task['start_time'] = datetime.now()

            for task in tasks:
                task['executor'].join()
                task['status'] = 'ending'
                task['end_time'] = datetime.now()

            overseer.join()

    def __cut__(self, time_line: TimeLine):
        if self.__is_usable__:
            try:
                FFmpeg(
                    inputs={self.__path__: [
                        '-y', '-itsoffset', '00:00:00.100'
                    ]},
                    outputs={time_line.output_path: [
                        '-ss', time_line.start_time,
                        '-t', time_line.length_time,
                        '-vcodec', 'copy',
                        '-acodec', 'copy',
                        '-threads', '5',
                        '-v', 'warning'

                    ]}, executable=self.__ffmpeg_path__
                ).run(stdout=None)
            except Exception as error:
                print(error)
