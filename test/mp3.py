import os
import re
import eyed3


if __name__ == '__main__':
    path = r'E:\Download\小说'

    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)
        files = os.listdir(folder_path)
        file_count = len(files)

        for file in files:
            name = re.compile(r'\d+').findall(file)[0].zfill(3)
            title = f'{folder}.{name}'
            album = f'有声小说.{folder}'
            suffix = file.split('.')[-1]
            file_path = os.path.join(folder_path, file)
            new_file_path = os.path.join(folder_path, f'{name}.{suffix}')

            audio_file = eyed3.load(file_path)
            audio_file.initTag()

            audio_file.tag.title = title
            audio_file.tag.album = album
            audio_file.tag.save()

            os.rename(file_path, new_file_path)

