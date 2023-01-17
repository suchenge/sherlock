from modules.service import dictionary


search_result = dictionary.search('E:\\Music *.mp3')
for item in search_result:
    print(item)