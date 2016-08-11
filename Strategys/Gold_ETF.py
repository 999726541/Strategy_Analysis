#-*-coding:UTF-8 -*-

from Models.find_ma import MA_CALCULATOR
from Strategy import Strategy_Base
from Visualization import get_rid_unchanged,plot_return_beta
from pitcher import read_csv_excel


class GOLD_ETF(Strategy_Base):

    def if_bull(self,longest_period=0):
        # 返回新的牛市df
        for i in range(longest_period,len(self._df)):
            dd = self._df[i:i + 1]
            if (dd.ma_30_close[0] > dd.ma_120_close[0] and
                            dd.ma_12_close[0] > dd.ma_20_close[0] > dd.ma_30_close[0]) \
                    or (dd.ma_5_close[0] > dd.ma_12_close[0] > dd.ma_18_close[0] > dd.ma_30_close[0] and
                                dd.ma_30_close[0] > self._df.ma_30_close[i - 1]):
                self._df.loc[i:i + 1, ('bull')] = 1
        return self._df

    def if_bear(self,longest_period=0):
        # 返回熊市值
        for i in range(longest_period,len(self._df)):
            dd = self._df[i:i + 1]
            if (dd.close[0] < dd.ma_120_close[0] and
                        dd.ma_12_close[0] < dd.ma_60_close[0]) or \
                    (dd.close[0] < dd.ma_120_close[0] and
                                     dd.ma_5_close[0] < dd.ma_12_close[0] < dd.ma_18_close[0] < dd.ma_30_close[0]):
                self._df.loc[i:i + 1, 'bear'] = 1
        return self._df

    def if_monkey(self,longest_period=0):
        # 返回猴市
        for i in range(longest_period,len(self._df)):
            if self._df.bull[i] == 0 and self._df.bear[i] == 0:
                self._df.loc[i:i + 1, 'monkey'] = 1
        return self._df

    def _if_long(self, i):
        # 4个返回参数:
        '''
        Return with four parameter:     long,    invest_pct,     cash_used,  if_pct_long

        long: If long or not: True or False

        invest_pct: How much cash you perpared to used. a number range from 0 to 1, Total asset*invest_pct money will be
        Used for cash_used

        cash_used: how much percent money you used to long( when if_pct_long==1),
         or how many share you want to long ( when if_pct_long==0)

        if_pct_long:1 or 0
        '''
        # 牛市---------->
        if self._df.bull[i] == 1 and \
                        self._df.ma_5_close[i] > self._df.ma_5_close[i - 1] and \
                        self._df.ma_5_close[i - 1] < self._df.ma_5_close[i - 2]:
            self._df.loc[i:i + 1, 'long'] = 1
            return True, 1, 1, 1
            # self._position(bull_long[0],bull_long[1],i,if_pct=if_pct)

        # 猴市---------->
        if self._df.monkey[i] == 1 and \
                        self._df.ma_12_close[i] > self._df.ma_12_close[i - 1] and \
                        self._df.ma_12_close[i - 1] < self._df.ma_12_close[i - 2]:
            self._df.loc[i:i + 1, 'long'] = 1
            return True, 1, 1, 1
        # 熊市---------->
        else:
            return False, 1, 1, 1

    def _if_short(self, i):
        '''
        Return 3 param:     short,  short_nub,  if_pct_short
        :short: True or False
        :short_numb: how much percent share you want to short(if_pct_short=1)
                     how many shares you want to short(if_pct_short=0)
        :if_pct_short: 0 or 1
        '''
        # 牛市---------->
        if self._df.bull[i] == 1 and \
                (self._df.ma_5_close[i] < self._df.ma_16_close[i] and self._df.ma_5_close[i - 1] > self._df.ma_16_close[
                        i - 1]):
            self._df.loc[i:i + 1, 'short'] = 1
            return True, 1, 1
        # 熊市---------->
        # 猴市---------->
        elif self._df.monkey[i] == 1 and \
                        self._df.ma_12_close[i] < self._df.ma_12_close[i-1] and \
                        self._df.ma_12_close[i - 1] > self._df.ma_12_close[i - 2]:
            self._df.loc[i:i + 1, 'short'] = 1
            return True, 1, 1
        else:
            return False, 1, 1

if __name__=='__main__':
    df = read_csv_excel('/Users/leotao/Downloads/黄金ETF回测.xlsx','择时分析-创')
    #df = ts.get_hist_data('160719')
    #print(df)
    df = MA_CALCULATOR(df)
    df = df.get_ma(ll=[5,12,13,16,18,20,30,60,120])
    test = GOLD_ETF(df)
    result = test.backtest(longest_period=120)
    print('start date: ' + test.start_date)
    pgraph = get_rid_unchanged(result)
    plot_return_beta(pgraph)
    #test.today_signal(120)


