import ssl
import urllib.request

from modules.av.collate.collator import Collator, FileType
from modules.download.creeper import Creeper


# 抓取图片程序
# Creeper().run()

# 整理文件程序
file_type = FileType.FILE
# path_param = ["F:\软件\Done\BGSD-410.mp4", "F:\软件\Done\REBDB-169.mkv", "F:\软件\Done\MBRAP-023", "F:\软件\Done\GASO-0011"]
path_param = "G:\\传输\\视频\\259LUXU-1024.mp4"
# path_param = "F:\软件\Done\MBRAP-023"

# file_type = FileType.DIR
# path_param = "F:\软件\Done"

Collator(path_param, file_type).run()
