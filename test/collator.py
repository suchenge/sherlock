from modules.service.movie_warehouse.collate.collator import Collator

path_param = r"D:\Project\split move\种子\003.warehouse"
# path_param = "F:\软件\Done\MBRAP-023"
# path_param = ["E:\\Picture\\BAKU-005.mp4", "E:\\Picture\\CJOD-310.mp4", "E:\\Picture\\JUFE-338"]


Collator(path_param).run()
