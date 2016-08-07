from pyalgotrade.tools import yahoofinance
from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import ma
import logging
import tushare as ts
import pandas
#yahoofinance.download_daily_bars('orcl',2015,'orcl-2015.csv')
#df = ts.get_hist_data('000001')
#df.to_csv('000001.csv')


logging.basicConfig(filename='log.txt',filemode='a',level=logging.DEBUG)
class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument,period_1,period_2):
        strategy.BacktestingStrategy.__init__(self, feed,1000)
        # We want a 15 period SMA over the closing prices.
        #self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), period)
        self.__instrument = instrument
        self.__position = None
        #self.setUseAdjustedValues(True)
        self.__feed = feed
        self.__time1 = period_1
        self.__time2 = period_2
        self._t1 = ma.SMA(self.__feed[self.__instrument].getCloseDataSeries(), self.__time1)
        self._t2 = ma.SMA(self.__feed[self.__instrument].getCloseDataSeries(), self.__time2)

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        #self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        #self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        if self._t2[-1] is None:
            return

        bar = bars[self.__instrument]
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if self._t1[-1] > self._t2[-1]:
                # Enter a buy market order for 10 shares. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, 50, True)
        # Check if we have to exit the position.
        elif self._t1[-1] < self._t2[-1] and not self.__position.exitActive():
            self.__position.exitMarket()

def run_strategy(smaPeriod,t2):
    # Load the yahoo feed from the CSV file
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV("test", "000001.csv")
    # Evaluate the strategy with the feed.
    myStrategy = MyStrategy(feed, "test", smaPeriod,t2)
    #print "Initial portfolio value: $%.2f" % myStrategy.getBroker().getEquity()
    myStrategy.run()
    if myStrategy.getBroker().getEquity() >=1000:
        print("Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity())
        print(smaPeriod,t2)

for i in range(1,10):
    for j in range(i+1,50):
        run_strategy(i,j)

#run_strategy(5,15)