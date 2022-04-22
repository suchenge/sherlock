from modules.av.collate.collator import Collator, FileType

file_type = FileType.FILE

path_param = "E:\\Temp\Done\\SSR-005.mp4"
# path_param = "F:\软件\Done\MBRAP-023"
# path_param = ["E:\\Picture\\BAKU-005.mp4", "E:\\Picture\\CJOD-310.mp4", "E:\\Picture\\JUFE-338"]


Collator(path_param, file_type).run()
