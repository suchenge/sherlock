import os

from modules.service.download.cartoon.strategy.provider import CartoonStrategyProvider
from modules.tools.http_request.http_client import HttpClient


def __get_picture_suffix__(image_url):
    picture_name = os.path.split(image_url)[-1]
    picture_suffix = picture_name.split(".")[-1]

    if picture_suffix == 'webp':
        picture_suffix = 'jpg'
    return picture_suffix


if __name__ == '__main__':
    urls = [
        'https://186sky.com/manga-info/5701183',
    ]

    for url in urls:
        strategy = CartoonStrategyProvider.get_strategy(url)

        if strategy is not None:
            title = strategy.get_title()
            images = strategy.get_image()

            save_folder = f'/Users/vito/Downloads/Picture/Cartoon/{title}'

            save_images = []

            for index in range(len(images)):
                image_info = images[index]

                name = image_info['name']
                url = image_info['url']

                image_path = fr'{save_folder}/{name}.{str(index).zfill(5)}.{__get_picture_suffix__(url)}'

                image = {
                    'path': image_path,
                    'url': url
                }

                HttpClient.download(**image)


