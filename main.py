import datetime
import os.path

from modules.migration.hamal import Hamal
from modules.migration.pathfinder import Pathfinder

def copy_file(source_path, target_path):
    counter = 0
    start_time = datetime.datetime.now()
    with open(source_path, 'rb') as source_file, open(target_path, 'wb+') as target_file:
        print('\rsource_size:' + str(os.path.getsize(source_path)))
        current_size = os.path.getsize(target_path)
        print('current_size:' + str(current_size))
        while True:
            current_time = datetime.datetime.now()
            if (current_time - start_time).seconds >= 5:
                print('current_size:' + str(current_size))
                start_time = current_time

            source_data = source_file.read(1024*1024*10)
            if not source_data:
                break

            target_file.write(source_data)
            current_size += len(source_data)
            counter = counter + 1

    source_file.close()
    target_file.close()
    print('target_size:' + str(os.path.getsize(target_path)))
    print('------------------\r' + str(counter))

'''
sources = 'H:\影视'
target = 'G:\影视'

Pathfinder(sources, target).pathfinding()


source_path = r'G:\影视\收藏\剧集\北京人在纽约\11.ts'
target_path = r'G:\北京人在纽约.11.ts'

copy_file(source_path, target_path)
'''