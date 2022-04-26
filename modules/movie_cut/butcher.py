import concurrent.futures

from ffmpy import FFmpeg
from datetime import datetime
from moviepy.editor import *
from modules.movie_cut.file import File


def computation_time(fun):
    def wrapper(*args, **kwargs):
        begin = datetime.now()
        index = args[1]

        fun(*args, **kwargs)

        end = datetime.now()
        seconds = (end - begin).seconds
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        print("%s|%02d:%02d:%02d" % (int(index) + 1, h, m, s))

    return wrapper


class Butcher(object):
    def __init__(self, path):
        self.__file__ = File(path)

        types = ['mkv', 'mp4', 'avi', 'wmv']
        if self.__file__.type.lower() not in types:
            return

        self.__ffmpeg_path__ = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ffmpeg.exe')

        if not os.path.exists(self.__ffmpeg_path__):
            return

        self.__timers__ = self.__get_timers__()

    def __get_timers__(self):
        timers = []
        timer_path = os.path.join(self.__file__.folder, self.__file__.title + '.txt')

        if not os.path.exists(timer_path):
            return

        with open(timer_path, 'r') as fs:
            while True:
                line = fs.readline()

                if not line:
                    break

                lines = line.split(' ')
                timers.append({'start': lines[0].replace('.', ':'), 'end': lines[1].replace('.', ':')})

        return timers

    def chop(self):
        try:
            for index in range(0, len(self.__timers__)):
                self.__chop__(index)

        except Exception as error:
            raise error

    @computation_time
    def __chop__(self, timer_index):
        output_name, output_path, start_time, end_time, length_time = self.__get_video_info__(timer_index)

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

        print(ffmpeg.cmd)
        ffmpeg.run(stdout=None)

    def __get_video_info__(self, timer_index):
        name_length = len(self.__timers__)
        if name_length < 5:
            name_length = 5

        output_name = '%s_%s.%s' % (self.__file__.title, str(timer_index + 1).zfill(name_length), self.__file__.type)
        output_path = os.path.join(self.__file__.folder, output_name)

        start_time = self.__timers__[timer_index]['start'].strip()
        end_time = self.__timers__[timer_index]['end'].strip()

        start_datetime = datetime.strptime(start_time, '%H:%M:%S')
        end_datetime = datetime.strptime(end_time, '%H:%M:%S')

        length_time_seconds = (end_datetime - start_datetime).seconds
        length_time_minute, length_time_second = divmod(length_time_seconds, 60)
        length_time_hour, length_time_minute = divmod(length_time_minute, 60)

        length_time = '%02d:%02d:%02d' % (length_time_hour, length_time_minute, length_time_second)

        print('%s|%s|%s|%s|' % (output_name, start_time, end_time, length_time))
        return output_name, output_path, start_time, end_time, length_time
