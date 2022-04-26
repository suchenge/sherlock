from modules.av.collate.marauder.javdb import MarauderJavdb


def get_marauder(file, request):
    return MarauderJavdb(file, request)
