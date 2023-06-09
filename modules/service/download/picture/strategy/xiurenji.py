from modules.service.download.picture.strategy.base import Base

def build(url, html):
    return Xiurenji(url, html)

class Xiurenji(Base):
    def __init__(self, url, html):
        super().__init__(url, html)

    def get_title(self):
        return self.__html__.xpath("//div[@class='title']/text()")[-1]
