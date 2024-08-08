from modules.service.movie_library.archive.archive import Archive


class File(Archive):
    def __init__(self, path):
        super(File, self).__init__(path)