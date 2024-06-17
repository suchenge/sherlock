from modules.service.download.cartoon.strategy.sky import SkyCartoonStrategy


class CartoonStrategyProvider(object):
    __strategies__ = [SkyCartoonStrategy]

    @staticmethod
    def get_strategy(url):
        for strategy in CartoonStrategyProvider.__strategies__:
            if strategy.is_match(url):
                return strategy(url)
