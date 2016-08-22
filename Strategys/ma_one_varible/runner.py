# -*- coding:utf-8 -*-

from Strategys.ma_one_varible.one_ma_factorial import test_
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

def date_incresed():
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
        write_to_mongo(rr, db='MA_testback', collection='Single_MA_90_increase', id=str(end))


#---------------------------Runner-----------------------

fixed_90()