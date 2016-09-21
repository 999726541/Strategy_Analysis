# -*- coding:utf-8 -*-

import pandas as pd

from Strategys.ma_one_varible.one_ma_factorial import test_,hs_300_strategy
from pitcher import get_his_data,write_to_mongo


#--------------------------------fixed_90_days_ma-----------------

def fixed_90():
    ma = [i+1 for i in range(120)]
    print(ma)
    df_all = get_his_data('hs300', ma=ma)
    length = len(df_all)
    for i in range(length-89):
        df = df_all[i:i+90]
        start = df.index[0]
        end = df.index[len(df)-1]
        print('start calculate :'+str(start)+' to '+str(end))
        rr = test_(ma, df)
        write_to_mongo(rr,db='MA_testback',collection='Single_MA_90_rolling',id=str(end))


#--------------------------------increased_days_ma-----------------

def date_accmulation():
    ma = [i + 1 for i in range(120)]
    print(ma)
    df_all = get_his_data('hs300', ma=ma)
    length = len(df_all)
    for i in range(length-29):
        df = df_all[:i + 30]
        start = df.index[0]
        end = df.index[len(df) - 1]
        print('start calculate :' + str(start) + ' to ' + str(end))
        rr = test_(ma, df)
        write_to_mongo(rr, db='Single_MA_testback', collection='2016-08-31', id=str(end))

# ----------------------------------------最近日,所有均线策略合集----------------
def date_accmulation_getall(today):
    ma = [i  for i in range(2,241)]
    df_all = get_his_data('000300', ma=ma,index=True)
    test = hs_300_strategy(df_all)
    for ii in ma:
        print('processing MA_'+str(ii))
        test.backtest(ma_1=str(ii),ma_2=str(ii))
        # return原始是1,100%
        df = pd.concat([test._df.position,test._df['return'],test._df.beta,test._df.drawdown,test._df.long,
                        test._df.short],axis=1)
        write_to_mongo(df, db='Single_MA_testback', collection=today, id='MA_'+str(ii))
        test = hs_300_strategy(df_all)
#---------------------------Runner-----------------------

date_accmulation_getall('2016-09-06')