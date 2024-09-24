from modules.service.download.picture.image import Image


class BaseSaver(object):
    def __init__(self):
        pass

    def query(self, main_url: str) -> list[Image]:
        pass

    def delete(self, image_url: str):
        pass

    def delete_batch(self, image_urls: list[str]):
        pass

    def remove_one(self, image: Image):
        pass

    def insert(self, image: Image):
        pass

    def insert_by_batch(self, images: list[Image]):
        pass
