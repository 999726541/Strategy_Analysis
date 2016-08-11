#-*-coding:UTF-8 -*-

from Strategy import Strategy_Base
from Visualization import plot_return_beta,get_rid_unchanged
from pitcher import get_his_data


class NSDK(Strategy_Base):

    def if_bull(self,longest_period=0):
        # 返回新的牛市df
        for i in range(longest_period,len(self._df)):
            dd = self._df[i:i + 1]
            if dd.ma_60_close[0] > dd.ma_250_close[0] and \
                            dd.ma_120_close[0] > dd.ma_250_close[0]:
                self._df.loc[i:i + 1, ('bull')] = 1
        return self._df

    def if_bear(self,longest_period=0):
        # 返回熊市值
        for i in range(longest_period,len(self._df)):
            if self._df.bull[i] == 0:
                self._df.loc[i:i + 1, 'bear'] = 1
        return self._df

    def if_monkey(self,longest_period=0):
        # 返回猴市
        for i in range(longest_period,len(self._df)):
            if self._df.bull[i] == 0:
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
        #每个if都有一个else
        # 牛市---------->
        if self._df.bull[i] == 1:
            if self._df.ma_3_close[i] > self._df.ma_3_close[i - 1] and \
                        self._df.ma_3_close[i - 1] < self._df.ma_3_close[i - 2]:
                self._df.loc[i:i + 1, 'long'] = 1
                return True, 1, 1, 1
            else: return False,1,1,1

            # self._position(bull_long[0],bull_long[1],i,if_pct=if_pct)

        # 猴市---------->
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
        # 熊市---------->
        if self._df.bear[i] == 1 and self._df.ma_3_close[i] < self._df.ma_3_close[i - 1] :
            self._df.loc[i:i + 1, 'short'] = 1
            return True, 1, 1
        # 猴市---------->
        elif self._df.monkey[i] == 1 and self._df.ma_3_close[i] < self._df.ma_3_close[i - 1]:
            self._df.loc[i:i + 1, 'short'] = 1
            return True, 1, 1
        # 牛市---------->
        else:
            return False, 1, 1

    def backtest(self, longest_period=0):
        ###Order matters
        # longest_period=====>从哪里开始有MA
        self.if_bull(longest_period=longest_period)
        self.if_bear(longest_period=longest_period)
        self.if_monkey(longest_period=longest_period)
        self.long_or_short()
        self._equity()
        self._win_lose()
        self._drawdown()
        self._return_rate()
        self.long_short_count()
        self._beta()
        print('最大回撤:' + str(max(self.drawdown) * 100) + '%')
        print('买入信号统计:' + str(self.long_count))
        print('卖出信号统计:' + str(self.short_count))
        print('全仓平仓亏损:' + str(self.lost_rate))
        print('全仓平仓赢: ' + str(self.win_rate))
        print('最大回报:' + str((self._df['return'].max() - 1) * 100) + '%')
        print('最大亏损:' + str((self._df['return'].min() - 1) * 100) + '%')
        print('总回报:' + str(self._df[len(self._df) - 1:len(self._df)]['return']))
        return self._df

if __name__=='__main__':
    df = get_his_data('513100',ma=[3,60,120,250])
    print(df)
    #df = get_his_data('162411',ma=[4,5,13,12,20,30,60,120,18,14])
    print(df)
    test = NSDK(df)
    #print(test._df)
    pgraph = test.backtest()
    print('start date: ' + test.start_date)
    test._df.to_csv('test3.csv')
    #test.coef_find()
    pgraph = get_rid_unchanged(pgraph)
    plot_return_beta(pgraph)