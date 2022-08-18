import re
import os
import threading

from ffmpy import FFmpeg
from datetime import datetime
from modules.movie_cut.file import File
from modules.movie_cut.overseer import Overseer


def __format_time___(time):
    result = time
    if '.' in time:
        result = result.replace('.', ':')

    match = re.compile(r'(\d{2})(\d{2})(\d{2})').findall(time)
    if match:
        result = ':'.join(match[0])

    return result.strip()


class Butcher(object):
    def __init__(self, path):
        self.__file__ = File(path)
        self.__timer_path__ = os.path.join(self.__file__.folder, self.__file__.title + '.txt')

        types = ['mkv', 'mp4', 'avi', 'wmv']
        if self.__file__.type.lower() not in types:
            return

        self.__ffmpeg_path__ = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ffmpeg.exe')

        if not os.path.exists(self.__ffmpeg_path__):
            return

        self.__timers__ = self.__get_timers__()

    def __get_timers__(self):
        timers = []

        if not os.path.exists(self.__timer_path__):
            return

        with open(self.__timer_path__, 'r') as fs:
            while True:
                line = fs.readline()

                if not line:
                    break

                lines = line.split(' ')
                timers.append({'start': __format_time___(lines[0]), 'end': __format_time___(lines[1])})

        return timers

    def chop(self):
        tasks = []

        for index in range(0, len(self.__timers__)):
            timer_info = self.__get_video_info__(index)
            current_timer = datetime.now()

            tasks.append({'timer_info': timer_info,
                          'status': 'waiting',
                          'start_time': current_timer,
                          'end_time': current_timer,
                          'executor': threading.Thread(target=self.__chop__, args=[timer_info])
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

        os.remove(self.__file__.path)
        os.remove(self.__timer_path__)

    def __chop__(self, timer_info):
        try:
            output_name, output_path, start_time, end_time, length_time = timer_info

            ffmpeg = FFmpeg(
                inputs={self.__file__.path: [
                    '-y', '-itsoffset', '00:00:00.600'
                ]},
                outputs={output_path: [
                    '-ss', start_time,
                    '-t', length_time,
                    '-vcodec', 'copy',
                    '-acodec', 'copy',
                    '-threads', '5',
                    '-v', 'warning'

                ]}, executable=self.__ffmpeg_path__
            )

            # print(ffmpeg.cmd)
            ffmpeg.run(stdout=None)
        except Exception as error:
            print(error)

    def __get_video_info__(self, timer_index):

        output_name = '%s_%s.%s' % (self.__file__.title, str(timer_index + 1).zfill(5), self.__file__.type)
        output_path = os.path.join(self.__file__.folder, output_name)

        start_time = self.__timers__[timer_index]['start']
        end_time = self.__timers__[timer_index]['end']

        start_datetime = datetime.strptime(start_time, '%H:%M:%S')
        end_datetime = datetime.strptime(end_time, '%H:%M:%S')

        length_time_seconds = (end_datetime - start_datetime).seconds
        length_time_minute, length_time_second = divmod(length_time_seconds, 60)
        length_time_hour, length_time_minute = divmod(length_time_minute, 60)

        length_time = '%02d:%02d:%02d' % (length_time_hour, length_time_minute, length_time_second)

        # print('%s|%s|%s|%s|' % (output_name, start_time, end_time, length_time))
        return output_name, output_path, start_time, end_time, length_time
