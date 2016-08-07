#-*- coding:utf-8 -*-
import tushare as ts
import csv
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import datetime
from Strategy import Strategy_Base
import matplotlib.pyplot as plt



class hs_300_strategy(Strategy_Base):

    def if_bull(self):
        # 返回新的牛市df
        for i in range(len(self._df)):
            dd = self._df[i:i + 1]
            if (dd.ma_30_close[0] > dd.ma_120_close[0] and
                            dd.ma_12_close[0] > dd.ma_20_close[0] > dd.ma_30_close[0]) \
                    or (dd.ma_5_close[0] > dd.ma_12_close[0] > dd.ma_18_close[0] > dd.ma_30_close[0] and
                                dd.ma_30_close[0] > self._df.ma_30_close[i - 1]):
                self._df.loc[i:i + 1, ('bull')] = 1
        return self._df

    def if_bear(self):
        # 返回熊市值
        for i in range(len(self._df)):
            dd = self._df[i:i + 1]
            if (dd.close[0] < dd.ma_120_close[0] and
                        dd.ma_12_close[0] < dd.ma_60_close[0]) or \
                    (dd.close[0] < dd.ma_120_close[0] and
                                     dd.ma_5_close[0] < dd.ma_12_close[0] < dd.ma_18_close[0] < dd.ma_30_close[0]):
                self._df.loc[i:i + 1, 'bear'] = 1
        return self._df


    def if_monkey(self):
        #返回猴市
        for i in range(len(self._df)):
            if self._df.bull[i] == 0 and self._df.bear[i] == 0:
                self._df.loc[i:i + 1, 'monkey'] = 1
        return self._df

    def _if_long(self,i):#TODO set more infom @ position
        #牛市---------->
        if self._df.bull[i] ==1 and \
            self._df.ma_5_close[i] > self._df.ma_5_close[i-1] and \
            self._df.ma_5_close[i-1] < self._df.ma_5_close[i-2]:
            self._df.loc[i:i + 1, 'long'] = 1
            return 1,3
            #self._position(bull_long[0],bull_long[1],i,if_pct=if_pct)

        #猴市---------->
        elif  self._df.monkey[i] ==1 and \
            self._df.ma_12_close[i] > self._df.ma_12_close[i-1] and \
            self._df.ma_12_close[i-1] < self._df.ma_12_close[i-2]:
            self._df.loc[i:i + 1, 'long'] = 1
            return 1,2

        #熊市---------->
        elif i < 11: return 0,0
        elif self._df.bear[i]==1 and \
            self._df.ma_5_close[i] > self._df.ma_18_close[i] and \
            self._df.ma_5_close[i-1] < self._df.ma_18_close[i-1] and \
                self._df.ma_5_close[i] > self._df.ma_5_close[i-1] and \
                (self._df.ma_30_close[i] - self._df.ma_30_close[i-10])/self._df.ma_30_close[i] > -0.07:
            self._df.loc[i:i + 1, 'long'] = 1
            return 1,1
        else: return 0,0


    def _if_short(self,i):#TODO
        # 牛市---------->
        if self._df.bull[i] ==1 and \
            (self._df.ma_5_close[i] < self._df.ma_20_close[i] and self._df.ma_5_close[i-1] > self._df.ma_20_close[i-1]):
            self._df.loc[i:i + 1, 'short'] = 1
            return 2,3
        # 熊市---------->
        elif self._df.bear[i] ==1 and \
            self._df.ma_5_close[i] < self._df.ma_5_close[i - 1] and \
            self._df.ma_5_close[i - 1] > self._df.ma_5_close[i - 2]:
            self._df.loc[i:i + 1, 'short'] = 1
            return 2,1
        # 猴市---------->
        elif self._df.monkey[i] ==1 and \
            self._df.ma_5_close[i] < self._df.ma_13_close[i] and \
            self._df.ma_5_close[i-1] > self._df.ma_13_close[i-1]:
            self._df.loc[i:i + 1, 'short'] = 1
            return 2,2
        else:
            return 0,0

    '''def long_or_short(self,bull=[1,1,1],monkey=[1,1,1],bear=[1,1,1],if_pct=1):#TODO inherit more info from long & short
        #if_pct=1,以资金为单位,每次买入股票可以不是整数,仓位不为整数
        #if_pct=0,以单个股票为买入单位,每次买入股票是整数,仓位为整数,会有余钱产生
        #bull_long=[1,1,1],[分仓,每次买入百分比,每次卖出百分比],数值在0到1之间,1是满仓或者
        #if if_pct=0,bull_long=[1,1,1],[分仓,每次买入股票数,每次卖出股票数]
        for i in range(len(self._df)):
            self._df.loc[i :i + 1, 'cash'] = self.total_invest
            if i<= 1:continue
            a,b = self._if_long(i)
            c,d = self._if_short(i)
            ll = [bear] + [monkey] + [bull]
            if i==len(self._df)-1:continue
            if a==1:
                self._position(ll[b-1][0],ll[b-1][1],ll[b-1][2],i,if_pct=if_pct,long_short=1)
            if c==2:
                self._position(ll[d - 1][0], ll[d - 1][1], ll[d - 1][2], i, if_pct=if_pct, long_short=2)
            if a==0 and c==0:
                self._df.loc[i+1 :i + 2, 'position'] = self._df.position[i]'''


if __name__=='__main__':
    df = ts.get_hist_data('160416')
    test = hs_300_strategy(df)
    pgraph = test.backtest()
    test._df.to_csv('test2.csv')
    graph = pgraph.reset_index()
    i=0
    n=1
    length = len(graph)
    while i < length:
        #print(len(graph))
        while graph.equity[i] == graph.equity[n]:
            #print(graph.equity[i],graph.equity[n])
            graph = graph.drop(n)
            n+=1
            if n>=length:break
            #print(i)
            #print(n)
        i=n
        n+=1
        #print(i)
    graph.plot('date',['return','beta'])
    plt.show()