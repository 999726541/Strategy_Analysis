# -*- coding:utf-8 -*-

import datetime

import pandas as pd

from Strategy import Strategy_Base
from pitcher import get_his_data,write_to_mongo


class hs_300_strategy(Strategy_Base):
    def if_bull(self, longest_period=0):
        # 返回新的牛市df
        pass

    def if_bear(self, longest_period=0):
        # 返回熊市值
        pass

    def if_monkey(self, longest_period=0):
        # 返回猴市
        pass

    def _if_long(self, i, ma_1, ma_2):
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
        if self._df['ma_' + ma_1 + '_close'][i] > self._df['ma_' + ma_1 + '_close'][i-1] and \
                        self._df['ma_' + ma_1 + '_close'][i - 1] <= self._df['ma_' + ma_1 + '_close'][i - 2]:
            return True, 1, 1, 1
            # self._position(bull_long[0],bull_long[1],i,if_pct=if_pct)
        else:
            return False, 1, 1, 1

    def _if_short(self, i, ma_1, ma_2):
        '''
        Return 3 param:     short,  short_nub,  if_pct_short
        :short: True or False
        :short_numb: how much percent share you want to short(if_pct_short=1)
                     how many shares you want to short(if_pct_short=0)
        :if_pct_short: 0 or 1
        '''
        # 牛市---------->
        if self._df['ma_' + ma_1 + '_close'][i] < self._df['ma_' + ma_1 + '_close'][i-1] and \
                        self._df['ma_' + ma_1 + '_close'][i - 1] >= self._df['ma_' + ma_1 + '_close'][i - 2]:
            return True, 1, 1
        else:
            return False, 1, 1

    def long_or_short(self, ma_1, ma_2):
        # if_pct=1,以资金为单位,每次买入股票可以不是整数,仓位不为整数
        # if_pct=0,以单个股票为买入单位,每次买入股票是整数,仓位为整数,会有余钱产生
        # invest_pct:愿意花总资金的多少做投资
        # cash_used:愿意每次买入多少,买入可以是一百分比资金为单位或者以股票为单位
        # short_nub:愿意卖出多少,卖出可以是一百分比资金为单位或者以股票为单位
        for i in range(len(self._df)):
            self._df.loc[i:i + 1, 'cash'] = self.total_invest
            #print(self._df.cash[i])
            long, invest_pct, cash_used, if_pct_long = self._if_long(i, ma_1=ma_1, ma_2=ma_2)
            short, short_nub, if_pct_short = self._if_short(i, ma_1=ma_1, ma_2=ma_2)

            if i == len(self._df) - 1: continue
            if short == True:
                self._position(short_pct=short_nub, i=i, if_pct=if_pct_short, long_short=2)
                self._df.loc[i:i+1,'short'] = 1
                continue
            if long == True:
                self._position(invest_pct=invest_pct, long_pct=cash_used, i=i, if_pct=if_pct_long, long_short=1)
                self._df.loc[i:i + 1, 'long'] = 1
                continue
            if long == False and short == False:
                self._df.loc[i + 1:i + 2, 'position'] = self._df.position[i]

    def backtest(self, ma_1, ma_2):
        ###Order matters
        self.if_bull()
        self.if_bear()
        self.if_monkey()
        self.long_or_short(ma_1=ma_1, ma_2=ma_2)
        self._equity()
        self._win_lose()
        self._drawdown()
        self._return_rate()
        self.long_short_count()
        self._beta()
        return pd.DataFrame(self._df[len(self._df) - 1:len(self._df)]['return'])

#########################____________________记得重新定义strategy函数!!!在loop strategy的时候
def test_(ma,df):
    test = hs_300_strategy(df)
    comb = []
    return_ = []
    drawback = []
    Beta = []
    for i in range(1, len(ma)):
            print('Process MA'+str(ma[i]))
            test.backtest(ma_1=str(ma[i]), ma_2=str(ma[i]))
            comb.append(str(ma[i]))
#不变为0,return, drawback,beta 都是 delta%变化
            return_.append(float(test._df[len(test._df)-1:len(test._df)]['return'][0]-1)*100)
            drawback.append(str(max(test._df.drawdown)*100))
            Beta.append((test._df[len(test._df)-1:len(test._df)]['beta'][0]-1)*100)
            test = hs_300_strategy(df)

    return pd.DataFrame({'MA':comb,'return':return_,'Beta':Beta,'drawback':drawback,
                         'start':test._df.index[0],'end':test._df.index[len(test._df)-1]}).set_index('MA')


if __name__ == '__main__':
    # df = get_his_data('hs300',ma = [5,12,13,18,20,30,60,120])
    # print(df)
    ma = [i+1 for i in range(120)]
    print(ma)
    start = datetime.datetime.strptime('2015-01-01','%Y-%m-%d')
    end = start+datetime.timedelta(90)
    df_all = get_his_data('hs300', ma=ma)
    while str(end) <= '2015-12-31':
        print('start calculate :'+str(start)[:10]+' to '+str(end)[:10])
        df = df_all[str(start)[:10]:str(end)[:10]]
        test_1 = hs_300_strategy(df)
        rr = test_(ma, df)
        write_to_mongo(rr,db='MA_testback',collection='Single_MA',id=str(start)[:10])
        start = start + datetime.timedelta(1)
        end = start + datetime.timedelta(90)

