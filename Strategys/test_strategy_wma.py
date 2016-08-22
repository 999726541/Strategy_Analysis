#-*- coding:utf-8 -*-

import pandas as pd

from Strategy import Strategy_Base
from pitcher import get_his_data_WMA


class hs_300_strategy(Strategy_Base):
    def __init__(self,df,invest=10000):
        super(hs_300_strategy,self).__init__(df,invest)
        #self._df['P_new'] = 0

    def if_bull(self,longest_period=0):
        # 返回新的牛市df
        pass

    def if_bear(self,longest_period=0):
        # 返回熊市值
        pass


    def if_monkey(self,longest_period=0):
        #返回猴市
        pass

    def _if_long(self,i,ma_1,ma_2):
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
        if  self._df['wma_'+ma_1+'_close'][i] > self._df['wma_'+ma_2+'_close'][i] and \
                        self._df['wma_'+ma_1+'_close'][i-1] < self._df['wma_'+ma_2+'_close'][i-1]:
            #self._df.loc[i:,'P_new'] = (self._df['wma_'+ma_1+'_close'][i]+self._df['wma_'+ma_2+'_close'][i]+
            #                            self._df['wma_' + ma_1 + '_close'][i - 1] + self._df['wma_' + ma_2 + '_close'][
            #                                i - 1])/4
            return True,1,1,1

        else:
            return False,1,1,1


    def _if_short(self,i,ma_1,ma_2):
        '''
        Return 3 param:     short,  short_nub,  if_pct_short
        :short: True or False
        :short_numb: how much percent share you want to short(if_pct_short=1)
                     how many shares you want to short(if_pct_short=0)
        :if_pct_short: 0 or 1
        '''
        # 牛市---------->
        if self._df['wma_' + ma_1 + '_close'][i] < self._df['wma_' + ma_2 + '_close'][i] and \
                        self._df['wma_' + ma_1 + '_close'][i - 1] > self._df['wma_' + ma_2 + '_close'][i - 1]:
            #self._df.loc[i:, 'P_new'] = 0
            return True, 1, 1
        #elif (self._df['wma_' + ma_1 + '_close'][i] + self._df['wma_' + ma_2 + '_close'][i])/2 < self._df['P_new'][i]:
            #self._df.loc[i:, 'P_new'] = 0
            #return True, 1, 1
        else:
            return False,1,1

    def long_or_short(self,ma_1,ma_2):
        # if_pct=1,以资金为单位,每次买入股票可以不是整数,仓位不为整数
        # if_pct=0,以单个股票为买入单位,每次买入股票是整数,仓位为整数,会有余钱产生
        # invest_pct:愿意花总资金的多少做投资
        # cash_used:愿意每次买入多少,买入可以是一百分比资金为单位或者以股票为单位
        # short_nub:愿意卖出多少,卖出可以是一百分比资金为单位或者以股票为单位
        for i in range(len(self._df)):
            self._df.loc[i:i + 1, 'cash'] = self.total_invest
            if i <= 1: continue

            short, short_nub, if_pct_short = self._if_short(i,ma_1=ma_1,ma_2=ma_2)
            if i == len(self._df) - 1: continue
            if short == True:
                self._position(short_pct=short_nub, i=i, if_pct=if_pct_short, long_short=2)
                self._df.loc[i:i + 1, 'short'] = 1
                continue

            long, invest_pct, cash_used, if_pct_long = self._if_long(i, ma_1=ma_1, ma_2=ma_2)
            if long == True:
                self._position(invest_pct=invest_pct, long_pct=cash_used, i=i, if_pct=if_pct_long, long_short=1)
                self._df.loc[i:i + 1, 'long'] = 1
                continue
            if long == False and short == False:
                self._df.loc[i + 1:i + 2, 'position'] = self._df.position[i]

    def backtest(self,ma_1,ma_2):
        ###Order matters
        self.if_bull()
        self.if_bear()
        self.if_monkey()
        self.long_or_short(ma_1=ma_1,ma_2=ma_2)
        self._equity()
        self._win_lose()
        self._drawdown()
        self._return_rate()
        self.long_short_count()
        self._beta()
        return ['return:'+str(self._df[len(self._df)-1:len(self._df)]['return'][0]),'最大回撤:'+str(max(self.drawdown)*100)+'%',
                'Beta:'+ str(self._df[len(self._df)-1:len(self._df)]['beta'][0])]


def test_(ma,dic,test):
    all_return = dic
    comb = []
    return_ = []
    drawback = []
    Beta = []
    for i in range(1, len(ma)):
        for k in range(i):
            all_return[str(ma[i]) + ',' + str(ma[k])] = test.backtest(ma_1=str(ma[k]), ma_2=str(ma[i]))
            #test._df.to_csv('test!!!'+str(i)+'.csv')
            comb.append(str(ma[i]) + ',' + str(ma[k]))
            return_.append(str((test._df[len(test._df)-1:len(test._df)]['return'][0]-1)*100)+'%')
            drawback.append(str(max(test._df.drawdown)*100)+'%')
            Beta.append(test._df[len(test._df)-1:len(test._df)]['beta'][0])
            test = hs_300_strategy(df)
            #print('Get result of (' + str(ma[i]) + ',' + str(ma[k]) + '):', end='')
            #print(all_return[str(ma[i]) + ',' + str(ma[k])])
    return pd.DataFrame({'comb':comb,'return':return_,'Beta':Beta,'drawback':drawback,
                         'start':test._df.index[0],'end':test._df.index[len(test._df)-1]})



if __name__=='__main__':
    wma = [5, 7, 10, 20, 30, 60, 120, 240]
    df = get_his_data_WMA('hs300',wma=wma,start='2014-01-01',end='2014-03-31')
    test_1 = hs_300_strategy(df)
    all_return_1 = {}
    resu = test_(wma,all_return_1,test_1)
    resu.to_csv('wma_test_result.csv',mode='a')

    df = get_his_data_WMA('hs300', wma=wma, start='2014-04-01', end='2014-06-31')
    test_1 = hs_300_strategy(df)
    all_return_1 = {}
    resu = test_(wma, all_return_1, test_1)
    resu.to_csv('wma_test_result.csv', mode='a')

    df = get_his_data_WMA('hs300', wma=wma, start='2014-07-01', end='2014-09-31')
    test_1 = hs_300_strategy(df)
    all_return_1 = {}
    resu = test_(wma, all_return_1, test_1)
    resu.to_csv('wma_test_result.csv', mode='a')

    df = get_his_data_WMA('hs300', wma=wma, start='2014-10-01', end='2014-12-31')
    test_1 = hs_300_strategy(df)
    all_return_1 = {}
    resu = test_(wma, all_return_1, test_1)
    resu.to_csv('wma_test_result.csv', mode='a')

    df = get_his_data_WMA('hs300', wma=wma, start='2015-01-01', end='2015-03-31')
    test_1 = hs_300_strategy(df)
    all_return_1 = {}
    resu = test_(wma, all_return_1, test_1)
    resu.to_csv('wma_test_result.csv', mode='a')

    df = get_his_data_WMA('hs300', wma=wma, start='2015-04-01', end='2015-06-31')
    test_1 = hs_300_strategy(df)
    all_return_1 = {}
    resu = test_(wma, all_return_1, test_1)
    resu.to_csv('wma_test_result.csv', mode='a')

    df = get_his_data_WMA('hs300', wma=wma, start='2015-07-01', end='2015-09-31')
    test_1 = hs_300_strategy(df)
    all_return_1 = {}
    resu = test_(wma, all_return_1, test_1)
    resu.to_csv('wma_test_result.csv', mode='a')

    df = get_his_data_WMA('hs300', wma=wma, start='2015-10-01', end='2015-12-31')
    test_1 = hs_300_strategy(df)
    all_return_1 = {}
    resu = test_(wma, all_return_1, test_1)
    resu.to_csv('wma_test_result.csv', mode='a')

    df = get_his_data_WMA('hs300', wma=wma, start='2016-01-01', end='2016-03-31')
    test_1 = hs_300_strategy(df)
    all_return_1 = {}
    resu = test_(wma, all_return_1, test_1)
    resu.to_csv('wma_test_result.csv', mode='a')

    df = get_his_data_WMA('hs300', wma=wma, start='2016-04-01', end='2016-06-31')
    test_1 = hs_300_strategy(df)
    all_return_1 = {}
    resu = test_(wma, all_return_1, test_1)
    resu.to_csv('wma_test_result.csv', mode='a')

    df = get_his_data_WMA('hs300', wma=wma, start='2016-07-01')
    test_4 = hs_300_strategy(df)#
    all_return_4 = {}
    resu = test_(wma, all_return_4, test_4)
    resu.to_csv('wma_test_result.csv', mode='a')