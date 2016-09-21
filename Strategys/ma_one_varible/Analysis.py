# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import pylab

from pitcher import read_mongo


def sort_df_index(df):
    #reset index for MA
    df = df.reset_index()
    df['index'] = df['index'].apply(int)
    df = df.set_index('index').sort_index()
    return df


def return_delta(df):
    #随着净资产增加 alpha 倍数,波动也会增加相应倍数,为了消除这个倍数影响,除以 t-1的alpha
    dd = pd.DataFrame(df['return']).diff()
    # 除以上一次的t-1时间的return
    for i in range(1,len(dd)-1):
        dd.loc[i:i+1,'return'] = dd['return'][i]/df['return'][i-1]
    dd = dd.rename(columns={'return':'delta_return'})
    combine = pd.concat([df,dd],axis=1)
    combine = combine[1:]
    return combine

def acf_check(data):
    #data is numpy type
    data = data - np.mean(data)
    data_draw = np.correlate(data,data,mode='full')
    print(len(data_draw))
    mid = data_draw[int((len(data_draw)-1)/2)]
    data_draw = data_draw/mid
    pylab.plot(data_draw)


def find_ma_strategy(ma,date):
    assert type(ma) is list
    records = []
    for i in ma:
        record = read_mongo(db='Single_MA_testback', collection=date, query={'_id': 'MA_'+str(i)})[0]
        records.append(record)
    return records

def find_delta_return_ave(df):
    ave = pd.DataFrame(df['delta_return'])
    ave['ave']=0
    #print(ave)
    length = len(df)-1
    row = 0
    i=0
    while i < length:
        if ave['delta_return'][i]  == 0:
            i+=1
            continue
        else:
            k=i+1
            while k<= length:
                if ave['delta_return'][k] == 0:
                    ave.loc[i:k,'ave']=ave['delta_return'][i:k].mean()
                    i=k
                    break
                elif k == length:
                    ave.loc[i:, 'ave'] = ave['delta_return'][i:].mean()
                    i = k
                    break
                k+=1
        i+=1
    return pd.concat([df,pd.DataFrame(ave['ave'])],axis=1)



def draw_delta_return_ave(ma,start = None, end = None):
    assert type(ma) is int
    #直接画图,画出delta ma strategy和delta ma 的ave,每次开仓的平均回报率
    alldata = find_ma_strategy([ma])
    data = return_delta(alldata[0])
    data = data[start:end]
    data.to_csv('888.csv')
    data = find_delta_return_ave(data)
    # data = get_rid_unchanged(data,'delta_return')
    data[['delta_return', 'ave']].plot()
    pylab.show()

def draw_acf(data):
    #data is numpy type
    data = data - np.mean(data)
    data_draw = np.correlate(data,data,mode='full')
    print('total number of point: '+str(len(data_draw)))
    mid = data_draw[int((len(data_draw)-1)/2)]
    data_draw = data_draw/mid
    pylab.plot(data_draw)
    pylab.show()

# -------------------------------------------------------#######-------------------------------------
#for ma in range(2,240):
#draw_delta_return_ave(20,start='2016-08-01',end='2016-08-20')


alldata = find_ma_strategy([i+2 for i in range(238)],date='2016-09-05')
##print(alldata[0])
#ave = {}
all_return = pd.DataFrame()
for element in range(len(alldata)):
    _return = alldata[element]['return']
    _return = _return.rename('ma_'+str(element+2))
    all_return = pd.concat([all_return,pd.DataFrame(_return)],axis=1)
all_return.to_csv('今天240天均线结果.csv')

#    data = return_delta(alldata[element])
#    data = data['2015-01-01':'2015-12-31']
#    #data['return'].plot()
#    #pylab.show()
#
#    data = find_delta_return_ave(data)
#    data = get_rid_unchanged(data,'ave')
#    data = get_rid_Zero(data,'ave')
#    #print(data)
#
#    #print(data)
#    #data.to_csv('results2.csv')
#    # draw acf
#    # npdata = data['ave']
#    # draw_acf(npdata)
#    ave[element+2] = [data['ave'].mean()]
#print(pd.DataFrame(ave).T)
#pd.DataFrame(ave).T.to_csv('result.csv')
