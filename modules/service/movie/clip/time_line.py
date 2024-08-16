import os

from datetime import datetime

from modules.service.movie.video.video_file import VideoFile


class TimeLine(object):
    def __init__(self, video: VideoFile, timer_index: int, timer):
        self.__output_name__ = '%s_%s.%s' % (video.title, str(timer_index + 1).zfill(5), video.type)
        self.__output_path__ = os.path.join(video.path, self.__output_name__)

        self.__start_time__ = timer['start']
        self.__end_time__ = timer['end']

        start_datetime = datetime.strptime(self.__start_time__, '%H:%M:%S')
        end_datetime = datetime.strptime(self.__end_time__, '%H:%M:%S')

        length_time_seconds = (end_datetime - start_datetime).seconds
        length_time_minute, length_time_second = divmod(length_time_seconds, 60)
        length_time_hour, length_time_minute = divmod(length_time_minute, 60)

        self.__length_time__ = '%02d:%02d:%02d' % (length_time_hour, length_time_minute, length_time_second)

    @property
    def output_name(self):
        return self.__output_name__

    @property
    def output_path(self):
        return self.__output_path__

    @property
    def start_time(self):
        return self.__start_time__

    @property
    def end_time(self):
        return self.__end_time__

    @property
    def length_time(self):
        return self.__length_time__
