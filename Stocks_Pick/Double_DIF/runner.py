# -*- coding:utf-8 -*-

import datetime

import pandas as pd

from Stocks_Pick.Double_DIF.Double_DIG_Ending_Price import BANKER_PRICE

# 说明
# --------------------------最近N天出现的最低价,设为天,则是3天之内出现的以双数结尾的最低价,写在等号之后
N = 4

# ---------------------------在K天回溯范围之内的最低价,一般50天之上,写在等号之后

K = 300

# ---------------------------不用动
picker = BANKER_PRICE()
dic = pd.DataFrame()
name = '庄家暗语' + str(datetime.datetime.today())
a = picker.find_long(lookback_days=N,total_range=K)
#print('出现双底股票数量: '+str(len(a)))
b = picker.find_short(lookback_days=N,total_range=K)
#print('出现双峰股票数量: '+str(len(b)))
a = pd.concat(a+[dic])
a.to_csv('long:'+name+'.csv')
b = pd.concat(b+[dic])
b.to_csv('short:'+name+'.csv')
# ---------------------------结束

