from modules.service.download.picture.strategy.spacemiss import Spacemiss
from modules.service.download.picture.strategy.xiurenbiz import Xiurenbiz
from modules.service.download.picture.strategy.xrmn import Xrmn
from modules.service.download.picture.strategy.sky import Sky


class ResolverStrategyProvider(object):
    __strategies__ = [Spacemiss, Xrmn, Xiurenbiz, Sky]

    @staticmethod
    def get_strategy(url, html):
        for strategy in ResolverStrategyProvider.__strategies__:
            if strategy.is_match(url, html):
                return strategy(url, html)

