from modules.service.movie_warehouse.collate.marauder.javdb import MarauderJavdb


def get_marauder(**kwargs):
    return MarauderJavdb(**kwargs)
