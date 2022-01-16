# 使用pyalgotrade 进行数据回撤， 详情：https://github.com/gbeced/pyalgotrade
import pyalgotrade

from pyalgotrade import strategy
from pyalgotrade.barfeed import quandlfeed
from pyalgotrade_tushare import tools,barfeed
from pyalgotrade.technical import ma

def safe_round(value, digits):
    if value is not None:
        value = round(value, digits)
    return value


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        self.__instrument = instrument
        # We want a 15 period SMA over the closing prices.
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 15)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info("%s %s" % (bar.getClose(), safe_round(self.__sma[-1], 2)))


# Load the bar feed from the CSV file
instruments=["000001"]
feeds=tools.build_feed(instruments, 2016, 2018, "histdata")
print(feeds)
# Evaluate the strategy with the feed's bars.
myStrategy = MyStrategy(feeds, instruments[0])
myStrategy.run()



