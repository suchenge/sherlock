from modules.service.download.picture.strategy.spacemiss import Spacemiss
from modules.service.download.picture.strategy.xrmn import Xrmn
from modules.service.download.picture.strategy.xiuren import Xiuren
from modules.service.download.picture.strategy.sky import Sky
from modules.service.download.picture.strategy.meitu8 import Meitu8
from modules.service.download.picture.strategy.dsws import Dsws


class ResolverStrategyProvider(object):
    __strategies__ = [Spacemiss, Xrmn, Sky, Xiuren, Meitu8, Dsws]

    @staticmethod
    def get_strategy(url):
        for strategy in ResolverStrategyProvider.__strategies__:
            if strategy.is_match(url):
                return strategy(url)
        return None

