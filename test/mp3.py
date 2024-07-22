import os
import re
import eyed3

def get_title(title):
    pattern = re.compile(r'(\d+)\.(.*?)\.mp3')
    find = pattern.findall(title)

    if len(find) > 0:
        result = pattern.findall(title)[0]
        return result[0].strip(), result[1].strip()
    else:
        return None, None


if __name__ == '__main__':
    path = r'E:\Music\综艺\高晓松\晓松奇谈'
    artist = '高晓松'
    album = '晓松奇谈'
    files = os.listdir(path)

    for file in files:
        file_path = os.path.join(path, file)
        suffix = file.split('.')[-1]

        # name = file.replace(f'.{suffix}', '').replace('[高质量]', '').replace('_标清', '').replace('_1080p', '').replace('_超清', '').strip()
        # index = name[0]
        # name = get_title(file)
        name = get_title(file)
        index = name[0]
        title = name[1]
        new_name = f'{str(index).zfill(3)}.{title}'
        # artist = name[0]

        if title is None or artist is None:
            continue


        new_file_path = os.path.join(path, f'{new_name}.{suffix}')

        audio_file = eyed3.load(file_path)
        audio_file.initTag()
        audio_file.tag.title = title
        audio_file.tag.artist = artist
        audio_file.tag.album = album
        audio_file.tag.save()

        if file_path != new_file_path:
            if os.path.exists(new_file_path) is False:
                os.rename(file_path, new_file_path)
            else:
                os.remove(file_path)


