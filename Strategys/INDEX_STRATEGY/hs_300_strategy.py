#-*- coding:utf-8 -*-

from Strategy import Strategy_Base
from Visualization import get_rid_unchanged_equity,plot_return_beta
from pitcher import get_his_data


class hs_300_strategy(Strategy_Base):

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
        #返回猴市
        for i in range(longest_period,len(self._df)):
            if self._df.bull[i] == 0 and self._df.bear[i] == 0:
                self._df.loc[i:i + 1, 'monkey'] = 1
        return self._df

    def _if_long(self,i):
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
        #牛市---------->
        if self._df.bull[i] ==1 and \
            self._df.ma_5_close[i] > self._df.ma_5_close[i-1] and \
            self._df.ma_5_close[i-1] < self._df.ma_5_close[i-2]:
            self._df.loc[i:i + 1, 'long'] = 1
            return True,1,1,1
            #self._position(bull_long[0],bull_long[1],i,if_pct=if_pct)

        #猴市---------->
        elif  self._df.monkey[i] ==1 and \
            self._df.ma_12_close[i] > self._df.ma_12_close[i-1] and \
            self._df.ma_12_close[i-1] < self._df.ma_12_close[i-2]:
            self._df.loc[i:i + 1, 'long'] = 1
            return True,1,1,1

        #熊市---------->
        elif self._df.bear[i]==1 and \
            self._df.ma_5_close[i] > self._df.ma_18_close[i] and \
            self._df.ma_5_close[i-1] < self._df.ma_18_close[i-1] and \
                self._df.ma_5_close[i] > self._df.ma_5_close[i-1] and \
                (self._df.ma_30_close[i] - self._df.ma_30_close[i-10])/self._df.ma_30_close[i] > -0.07:
            self._df.loc[i:i + 1, 'long'] = 1
            return True,1,1,1
        else: return False,1,1,1


    def _if_short(self,i):
        '''
        Return 3 param:     short,  short_nub,  if_pct_short
        :short: True or False
        :short_numb: how much percent share you want to short(if_pct_short=1)
                     how many shares you want to short(if_pct_short=0)
        :if_pct_short: 0 or 1
        '''
        # 牛市---------->
        if self._df.bull[i] ==1 and \
            (self._df.ma_5_close[i] < self._df.ma_20_close[i] and self._df.ma_5_close[i-1] > self._df.ma_20_close[i-1]):
            self._df.loc[i:i + 1, 'short'] = 1
            return True,1,1
        # 熊市---------->
        elif self._df.bear[i] ==1 and \
            self._df.ma_5_close[i] < self._df.ma_5_close[i - 1] and \
            self._df.ma_5_close[i - 1] > self._df.ma_5_close[i - 2]:
            self._df.loc[i:i + 1, 'short'] = 1
            return True,1,1
        # 猴市---------->
        elif self._df.monkey[i] ==1 and \
            self._df.ma_5_close[i] < self._df.ma_13_close[i] and \
            self._df.ma_5_close[i-1] > self._df.ma_13_close[i-1]:
            self._df.loc[i:i + 1, 'short'] = 1
            return True,1,1
        else:
            return False,1,1


if __name__=='__main__':
    df = get_his_data('hs300',start='2014-01-01',ma = [5,12,13,18,20,30,60,120])
    #print(df)
    #df = read_csv_excel('/Users/leotao/Downloads/沪深300回测.xlsx', '择时分析-创')
    #df = MA_CALCULATOR(df)
    #df = df.get_ma(ll = [5,12,13,18,20,30,60,120])
    test = hs_300_strategy(df)
    pgraph = test.backtest()
    print('start date: ' + test.start_date)
    test._df.to_csv('test2.csv')
    #test.coef_find()
    pgraph = get_rid_unchanged_equity(pgraph)
    plot_return_beta(pgraph)