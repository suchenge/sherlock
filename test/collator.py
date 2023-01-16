from modules.service.movie_warehouse.collate.collator import Collator
from modules.tools.exception_container.exception_list import ExceptionList

path_param = r"G:\传输\种子\temp"
# path_param = "F:\软件\Done\MBRAP-023"
# path_param = ["E:\\Picture\\BAKU-005.mp4", "E:\\Picture\\CJOD-310.mp4", "E:\\Picture\\JUFE-338"]

collator = Collator(path_param)
collator.run()

exception_container = ExceptionList()
has_errors = exception_container.empty()
exception_container.print()
