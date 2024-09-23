from modules.service.download.picture.image_information import ImageInformation


class BaseSaver(object):
    def __init__(self):
        pass

    def query(self, main_url: str) -> list[ImageInformation]:
        pass

    def delete_one(self, image_url: str):
        pass

    def remove_one(self, image: ImageInformation):
        pass

    def insert_by_batch(self, images: list[ImageInformation]):
        pass