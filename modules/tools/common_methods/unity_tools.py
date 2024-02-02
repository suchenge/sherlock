import platform


class UnityTools(object):
    def __int__(self):
        pass

    @staticmethod
    def is_mac_os():
        return platform.system() == 'Darwin'
