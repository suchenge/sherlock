import os

from pathlib import Path
from modules.migration.recorder import Recorder


class Pathfinder(object):
    def __init__(self, source_directory, target_directory):
        self.__source_directory__ = source_directory
        self.__target_directory__ = target_directory

        self.__recorder__ = Recorder(target_directory)

    def pathfinding(self):
        self.__recorder__.start()
        self.__scan_directory__(self.__source_directory__
                                , self.__target_directory__)

        self.__recorder__.stop()

    def __scan_directory__(self, source_directory, target_directory):
        if not os.path.exists(target_directory):
            Path(target_directory).mkdir(exist_ok=True)

        files = os.listdir(source_directory)
        for path in files:
            source_path = os.path.join(source_directory, path)
            target_path = os.path.join(target_directory, path)

            is_file = os.path.isfile(source_path)
            self.__recorder__.append(source_path, target_path, is_file)

            if is_file:
                self.__sign_file__(source_path, target_path)
            else:
                self.__scan_directory__(source_path, target_path)

    def __sign_file__(self, source_file, target_file):
        file_name = os.path.split(source_file)[1]
        target_path = os.path.split(target_file)[0] + '\\' +file_name + '.txt'

        file = open(target_path, 'w', encoding='utf-8')
        file.write('source_file:' + source_file + '\n' + 'source_size:' + str(os.stat(source_file).st_size))
        file.close()
