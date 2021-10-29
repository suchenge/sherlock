from modules.av.collate.collator import Collator, FileType

file_type = FileType.DIR
path_param = "E:\\Temp\\Done"

Collator(path_param, file_type).run()