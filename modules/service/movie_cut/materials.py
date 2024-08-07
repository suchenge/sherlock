import os
import re
import shutil
import threading

from ffmpy import FFmpeg
from datetime import datetime

from modules.service.movie_cut.file import File
from modules.service.movie_cut.blueprint import Blueprint
from modules.service.movie_cut.overseer import Overseer

from modules.service.movie_warehouse.collate.file import File as MovieFile
from modules.service.movie_warehouse.collate.porter import Porter
from modules.service.movie_warehouse.collate.marauder import marauder_factory

from modules.tools.http_request.request import Request
from modules.tools.thread_pools.task_pool import TaskPool
from modules.tools.common_methods.unity_tools import ffmpeg_execute_path


class Materials(File):
    def __init__(self, path):
        self.__is_usable__ = False
        file = File(path)

        if file.is_movie:
            super().__init__(path)

            self.__ffmpeg_path__ = ffmpeg_execute_path()
            self.__blueprint_file_path__ = f'{os.path.join(self.__folder__, self.__title__ + '.txt')}'
            self.__concat_file_path__ = f'{self.__path__}.merge.txt'
            self.__merge_file_path__ = f'{os.path.join(self.__folder__, self.__title__ + f'.merge.{self.__type__}')}'

            self.__blueprints__ = self.__build_blueprints__()
            if self.__blueprints__ is not None and len(self.__blueprints__) > 0:
                self.__is_usable__ = True

    @property
    def is_usable(self):
        return self.__is_usable__

    @property
    def blueprints(self):
        if self.__is_usable__:
            return self.__blueprints__
        else:
            return None

    def pigeonholed(self, request: Request):
        movie_file = MovieFile(self.__path__)

        marauder = marauder_factory.get_marauder(**{'file': movie_file, 'request': request})
        film = marauder.to_film()
        print('文件解析结果\n %s' % str(film))

        porter = Porter(film)
        porter.move()
        porter.save_poster(request)
        porter.save_stills(request)

        TaskPool.join()

        film_folder = movie_file.folder

        self.__move_file__(self.__blueprint_file_path__, film_folder)
        self.__move_file__(self.__concat_file_path__, film_folder)
        self.__move_file__(self.__merge_file_path__, film_folder)

        if self.__blueprints__ is not None and len(self.__blueprints__) > 0:
            for blueprint in self.__blueprints__:
                self.__move_file__(blueprint.output_path, film_folder)

    def __move_file__(self, source_path, target_folder):
        if os.path.exists(source_path):
            source_file = File(source_path)
            source_file_path = source_file.path
            target_file_path = f'{target_folder}/{source_file.name}'

            shutil.move(source_file_path, target_file_path)

    def merge(self):
        if self.__is_usable__ and len(self.__blueprints__) > 0:
            with open(self.__concat_file_path__, 'w', encoding='utf') as merge_file:
                for blueprint in self.__blueprints__:
                    merge_file.write(f'file \'{blueprint.output_path}\'')

            try:
                FFmpeg(
                    global_options=['-f', 'concat'],
                    inputs={self.__concat_file_path__: ['-safe', '0']},
                    outputs={self.__merge_file_path__: ['-c', 'copy']},
                    executable=self.__ffmpeg_path__
                ).run()

                os.remove(self.__concat_file_path__)

                for blueprint in self.__blueprints__:
                    os.remove(blueprint.output_path)

            except Exception as error:
                print(error)
        
    def clip(self):
        if self.__is_usable__:
            current_timer = datetime.now()
            tasks = []

            for blueprint in self.__blueprints__:
                tasks.append({
                                'timer_info': self.__build_timer_info__(blueprint),
                                'status': 'waiting',
                                'start_time': current_timer,
                                'end_time': current_timer,
                                'executor': threading.Thread(target=self.__clip__, args=[blueprint])
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

    def __build_timer_info__(self, blueprint: Blueprint):
        return blueprint.output_name, blueprint.output_path, blueprint.start_time, blueprint.end_time, blueprint.length_time
                
    def __clip__(self, blueprint: Blueprint):
        if self.__is_usable__:
            try:
                FFmpeg(
                    inputs={self.__path__: [
                        '-y', '-itsoffset', '00:00:00.600'
                    ]},
                    outputs={blueprint.output_path: [
                        '-ss', blueprint.start_time,
                        '-t', blueprint.length_time,
                        '-vcodec', 'copy',
                        '-acodec', 'copy',
                        '-threads', '5',
                        '-v', 'warning'

                    ]}, executable=self.__ffmpeg_path__
                ).run(stdout=None)
            except Exception as error:
                print(error)

    def __build_blueprints__(self):
        if os.path.exists(self.__blueprint_file_path__):
            blueprints = []
            index = 0
            with open(self.__blueprint_file_path__, 'r') as fs:
                while True:
                    line = fs.readline()

                    if not line:
                        break

                    lines = line.split(' ')
                    time = {
                        'start': self.__format_time___(lines[0]),
                        'end': self.__format_time___(lines[1]),
                    }
                    blueprints.append(Blueprint(self, index, time))
                    index += 1

            return blueprints

    def __format_time___(self, time):
        result = time
        if '.' in time:
            result = result.replace('.', ':')

        match = re.compile(r'(\d{2})(\d{2})(\d{2})').findall(time)
        if match:
            result = ':'.join(match[0])

        return result.strip()
