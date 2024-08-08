from modules.service.movie_library.archive.label import Label


class Archive(object):
    def __init__(self, path, analyst: Analyst):
        self.__label__ = None

    @property
    def label(self) -> Label:
        if self.__label__ is None:
            self.__label__ = Label()
        return self.__label__
