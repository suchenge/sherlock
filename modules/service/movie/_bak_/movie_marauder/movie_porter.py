import os

from modules.service.movie_marauder.movie_information import MovieInformation


class MoviePoster(object):
    def __init__(self, movie: MovieInformation, folder: str):
        self.__path__ = os.path.join(folder, movie.title)
        self.__movie__ = movie

    def save(self):
        pass