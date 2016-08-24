# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import pylab

from Visualization import get_rid_unchanged,get_rid_Zero
from pitcher import read_mongo


def sort_df_index(df):
    #reset index for MA
    df = df.reset_index()
    df['index'] = df['index'].apply(int)
    df = df.set_index('index').sort_index()
    return df


def return_delta(df):
    dd = pd.DataFrame(df['return']).diff()
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


def ma_compare(alldata,start,end):
    a_return, b_dlt = get_return_and_delta(alldata, ma=[i for i in range(2,121)])
    return a_return[start:end].T,b_dlt[start:end].T

def find_ma_strategy(ma):
    assert type(ma) is list
    records = []
    for i in ma:
        record = read_mongo(db='MA_testback', collection='Single_MA_accmulation_all', query={'_id': 'MA_'+str(i)+'_2016-08-24'})[0]
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



def draw_delta_return_ave(ma):
    assert type(ma) is int
    #直接画图,画出delta ma strategy和delta ma 的ave,每次开仓的平均回报率
    alldata = find_ma_strategy([ma])
    data = return_delta(alldata[0])
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
# for ma in range(2,240):
draw_delta_return_ave(44)


alldata = find_ma_strategy([44])
print(alldata[0])
data = return_delta(alldata[0])
data = data[:100]
data = find_delta_return_ave(data)
data = get_rid_unchanged(data,'ave')
data = get_rid_Zero(data,'ave')
#print(data)
npdata = data['ave']
#draw_acf(npdata)
print(data['ave'].mean())
