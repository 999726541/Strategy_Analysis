#-*- coding:utf-8 -*-
#现在就写了日线数据,这个strategy包括了基本的ma计算,熊牛定义
#!!!!!!!!!!!!!!!!!!!!!注意只写了日线数据的基本策略!!!!!!!!!!!!!!!
import pandas as pd
import tushare as ts


class Strategy_Base(object):
    def __init__(self,df,total_invest=10000):
        #Make sure it ranked with ascend with date,index=date
        self.initial_invest = total_invest
        self._df = df.sort_index()
        self._df['bull']=0
        self._df['bear'] = 0
        self._df['position'] = 0
        self._df['monkey'] = 0
        self._df['long'] = 0
        self._df['short'] = 0
        self._df['long_count']=0
        self._df['short_count']=0
        self._df['drawdown']=0
        self._df['equity']=0
        self._df['cash']=0
        self._df['beta']=1
        #self._df['total_equity'] = 0
        self._df['return'] = 1
        self.long_count=0
        self.short_count=0
        self.drawdown=[]
        self.code=''
        self.start_date = self._df.index[0] #index = date
        self.end_date = self._df.index[-1]
        self.win_count=0
        self.lost_count = 0
        self.win_rate=[]
        self.win_cash=[]
        self.lost_rate=[]
        self.lost_cash=[]
        self.total_invest=total_invest
        self.name = 'hs_300_strategy'
        self._long = 0
        self._short = 0
        #self.code = code


    def if_bull(self):
        #返回新的牛市df
        raise NotImplementedError

    def if_bear(self):
        #返回熊市值
        raise NotImplementedError

    def if_monkey(self):
        raise NotImplementedError

    def _if_long(self):
        raise NotImplementedError

    def _if_short(self):
        raise NotImplementedError

    def _position(self,invest_pct=1,long_pct=1,short_pct=1,i=None,if_pct=1,long_short=0):
        #long_short = 1 :long;
        #long_short = 2 :short;
        if if_pct == 1:
            if long_short==1:
                self._df.loc[i + 1:i + 2, 'position'] = self.total_invest*invest_pct*long_pct/self._df.open[i+1]+self._df.position[i]
                #print('Purchased stock: used '+str(self.total_invest*invest_pct*long_pct)+' cash')
                self.total_invest -= self.total_invest*invest_pct*long_pct
                #print('cash left:'+str(self.total_invest))

            if long_short==2:
                #如果以后可以做空,就把self._df.position[i]改成做空比率!!!!!!!
                self._df.loc[i+1:i+2,'position'] = self._df.position[i]-self._df.position[i]*short_pct
                #print('Sell stock: get' + str(self._df.open[i+1] * short_pct*self._df.position[i]) + ' cash')
                self.total_invest += self._df.open[i+1] * short_pct*self._df.position[i]
                #print('cash left:'+str(self.total_invest))



    def _equity(self):
        #算每日净值,equity=today_position*today_open_price
        for i in range(len(self._df)):
            self._df.loc[i:i+1,'equity'] = self._df.position[i]*self._df.open[i]+self._df.cash[i]


    def _drawdown(self):#checked
        #回撤%
        length = len(self._df)
        for i in range(len(self._df)):
            drawldown = round((self._df.equity[i] - self._df[i:length].equity.min()) / self._df.equity[i], 5)
            self._df.loc[i:i + 1, 'drawdown'] = drawldown
            self.drawdown.append(drawldown)
            #if self._df.position[i] != 0 and self._df.position[i-1] == 0:
             #   for k in range(i,len(self._df)):
              #      if self._df.position[k] == 0:
               #         for z in range(i,k):
                #            drawldown = round((self._df.equity[z] - self._df[z:k].equity.min())/self._df.equity[z],3)
                 #           self._df.loc[z:z+1,'drawdown']=drawldown
                  #          self.drawdown.append(drawldown)
                   #    break

    def _win_lose(self):
        inital,final=0,0
        for i in range( len(self._df)):
            if self._df.position[i]-self._df.position[i-1]>0:
                self.long_count+=1  #计算这是出现的第几次买入或者卖出
                self._long += 1
                self._df.loc[i:i + 1, 'long_count'] = self.long_count #long的次数
            if self._df.position[i] - self._df.position[i - 1] < 0:
                self.short_count += 1
                self._short += 1
                self._df.loc[i:i + 1, 'short_count'] = self.short_count #计算这是出现的第几次买入或者卖出
            if self._df.position[i] != 0 and self._df.position[i - 1] == 0:
                inital=i
            if self._df.position[i]==0 and self._df.position[i - 1] != 0:
                final=i
            if inital !=0 and final !=0:
                profit = self._df.equity[final] - self._df.equity[inital]
                if profit > 0:
                    self.win_count += 1
                    self.win_cash.append(profit)
                    self.win_rate.append(profit / self._df.equity[inital])
                else:
                    self.lost_cash.append(profit)
                    self.lost_count += 1
                    self.lost_rate.append(profit / self._df.equity[inital])
                inital, final = 0, 0


    def _return_rate(self):
        for i in range(len(self._df)):
            self._df.loc[i:i + 1, 'return'] = self._df.equity[i]/self.initial_invest


    def long_or_short(self):
        # if_pct=1,以资金为单位,每次买入股票可以不是整数,仓位不为整数
        # if_pct=0,以单个股票为买入单位,每次买入股票是整数,仓位为整数,会有余钱产生
        # invest_pct:愿意花总资金的多少做投资
        # cash_used:愿意每次买入多少,买入可以是一百分比资金为单位或者以股票为单位
        # short_nub:愿意卖出多少,卖出可以是一百分比资金为单位或者以股票为单位
        for i in range(len(self._df)):
            self._df.loc[i:i + 1, 'cash'] = self.total_invest
            if i <= 1: continue

            long,invest_pct, cash_used, if_pct_long = self._if_long(i)
            short, short_nub, if_pct_short = self._if_short(i)

            if i == len(self._df) - 1: continue
            if short == True:
                self._position(short_pct=short_nub,i=i,if_pct=if_pct_short, long_short=2)
                continue
            if long == True:
                self._position(invest_pct=invest_pct,long_pct=cash_used, i=i, if_pct=if_pct_long, long_short=1)
                continue
            if long == False and short == False:
                self._df.loc[i + 1:i + 2, 'position'] = self._df.position[i]

    def long_short_count(self):
        #计算所有出现的信号
        self.long_count = self._df.long.sum()
        self.short_count = self._df.short.sum()

    def _beta(self):
        for i in range(len(self._df)):
            self._df.loc[i:i+1,'beta']=self._df.close[i]/self._df.close[0]

    def backtest(self):
        ###Order matters
        self.if_bull()
        self.if_bear()
        self.if_monkey()
        self.long_or_short()
        self._equity()
        self._win_lose()
        #f.write('买入次数: '+str(self.long_count)+ '\n')
        ##f.write('卖出次数: '+str(self.short_count)+ '\n')
        self._drawdown()
        self._return_rate()
        self.long_short_count()
        self._beta()
        #f.write('信号个数: '+str(self.long_count+self.short_count)+'\n')
        #f.write('盈利次数: '+str(self.win_count)+ '\n')
        #f.write('单次全仓平仓赢: ' + str(max(self.win_rate))+ '\n')
        #f.write('单次全仓平仓亏损:' + str(max(self.lost_rate))+ '\n')
        #f.write('单次盈利占总盈利比: '+ str(max(self.win_cash)/sum(self.win_cash))+ '\n')
        #average_win = sum(self.win_cash) / len(self.win_cash)
        #average_lost = sum(self.lost_cash) / len(self.lost_cash)
        #f.write('平均盈利: ' + str(average_win)+'\n')
        #f.write('平均方差: ' + str(sum((i - average_win) ** 2 for i in self.win_cash) / len(self.win_cash))+ '\n')
        #f.write('平均亏损: '+ str(average_lost)+ '\n')
        #f.write('平均方差: ' + str(sum((i - average_lost) ** 2 for i in self.lost_cash) / len(self.lost_cash))+ '\n')
        #f.write('胜率: '+ str(len(self.win_cash)/(len(self.win_cash)+len(self.lost_cash)))+ '\n')
        #f.write('盈亏保障倍数: '+str(sum(self.win_cash)/sum(self.lost_cash))+ '\n')
        print('最大回撤:'+str(max(self.drawdown)*100)+'%')
        print('买入信号统计:'+str(self.long_count))
        print('卖出信号统计:' + str(self.short_count))
        print('全仓平仓亏损:' + str(self.lost_rate))
        print('全仓平仓赢: ' + str(self.win_rate))
        print('最大回报:'+str((self._df['return'].max()-1)*100)+'%')
        print('最大亏损:'+str((self._df['return'].min()-1)*100)+'%')
        print('总回报:'+str(self._df[len(self._df)-1:len(self._df)]['return']))
        return self._df

    def coef_find(self):
        dic = {}
        if len(self.win_cash) != 0:
            average_win = sum(self.win_cash) / len(self.win_cash)
            dic['平均盈利'] = [average_win]
            dic['平均盈利方差'] = [sum(abs(((i / average_win)) - 1) for i in self.win_cash) / len(self.win_cash)]
            dic['单次盈利占总盈利比'] = [max(self.win_cash) / sum(self.win_cash)]
            dic['单次全仓平仓赢'] = [max(self.win_rate)]
        if len(self.win_cash) == 0:
            dic['平均盈利'] = [0]
            dic['平均盈利方差'] = [0]
            dic['单次盈利占总盈利比'] = [0]
            dic['单次全仓平仓赢'] = [0]
        if len(self.lost_cash) !=0:
            average_lost = sum(self.lost_cash) / len(self.lost_cash)
            dic['平均亏损'] = [average_lost]
            dic['平均亏损方差'] = [sum((abs((i / average_lost) - 1)) for i in self.lost_cash) / len(self.lost_cash)]
            dic['单次全仓平仓亏损'] = [max(self.lost_rate)]
        if len(self.lost_cash) == 0:
            dic['平均亏损'] = [0]
            dic['平均亏损方差'] = [0]
            dic['单次全仓平仓亏损'] = [0]
        dic['信号个数'] = [self.long_count+self.short_count]
        dic['盈利次数'] = [self.win_count]
        #dic['单次全仓平仓赢'] = [max(self.win_rate)]
        #dic['单次全仓平仓亏损'] = [max(self.lost_rate)]
        #dic['单次盈利占总盈利比'] = [max(self.win_cash)/sum(self.win_cash)]
        #dic['平均盈利'] = [average_win]
        #dic['平均盈利方差'] = [sum(((i / average_win)-1) ** 2 for i in self.win_cash) / len(self.win_cash)]
        #dic['平均亏损'] = [average_lost]
        #dic['平均方差'] = [sum(((i / average_lost)-1) ** 2 for i in self.lost_cash) / len(self.lost_cash)]
        dic['胜率'] = [len(self.win_cash)/(len(self.win_cash)+len(self.lost_cash))]
        dic['盈亏保障倍数'] = [sum(self.win_cash)/sum(self.lost_cash)]
        dic['买入次数'] = [self._long]
        dic['卖出次数'] = [self._short]
        df = pd.DataFrame(dic)
        df.to_csv('Backtest_info.csv')
        #print(df)

    def today_signal(self):
        self.if_bull()
        self.if_bear()
        self.if_monkey()
        self.long_or_short()
        return self._df[len(self._df)-5:len(self._df)].loc[:,['monkey','bull','bear','long','short','close']]

if __name__=='__main__':
    df = ts.get_hist_data('160416','2015-07-27')
    #print(df)
    test = Strategy_Base(df)
    test.get_ma(ll=[5,12,18,20,30,60,120])
    test.if_bull()
    test.if_bear()
    mm = test.if_monkey()
    #mm.to_csv('test.txt')
    #print(mm.monkey)
