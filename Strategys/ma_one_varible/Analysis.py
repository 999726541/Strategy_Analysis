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


def find_all_return(alldata,ll=[0,10,20]):
    #输入一个DataFrame的list,输出所有df的return的一个Datafram
    length = len(alldata)
    combine = pd.DataFrame()
    for i in ll:
        df = alldata[i]
        date = df['end'][0]
        df = pd.DataFrame(df[['return']])
        name = str(date)
        df = df.rename(columns={'return':name})
        combine = pd.concat([combine,sort_df_index(df)],axis=1)
    return combine

def column_delta(df):
    combine=pd.DataFrame()
    title = list(df.columns)
    for i in range(len(title)-1):
        delta = pd.DataFrame(df[title[i+1]]-df[title[i]])
        name = title[i+1][:]
        delta = delta.rename(columns={0:name})
        combine = pd.concat([combine,delta],axis=1)
    return combine

def acf_check(data):
    #data is numpy type
    data = data - np.mean(data)
    data_draw = np.correlate(data,data,mode='full')
    print(len(data_draw))
    mid = data_draw[int((len(data_draw)-1)/2)]
    data_draw = data_draw/mid
    pylab.plot(data_draw)


def get_return_and_delta(alldata,ma=[]):
    #column name is ma
    zz = find_all_return(alldata,ll=[i for i in range(len(alldata))])
    zz_delta = column_delta(zz)
    return zz.T[ma],zz_delta.T[ma]


def ma_compare(alldata,start,end):
    a_return, b_dlt = get_return_and_delta(alldata, ma=[i for i in range(2,121)])
    return a_return[start:end].T,b_dlt[start:end].T


alldata = read_mongo(db='MA_testback', collection='Single_MA_90_rolling')
#print(len(alldata))
a_return,b_dlt = ma_compare(alldata,start=450,end=525)
#print(a_return.T)
a_return.plot(y=['2016-05-09','2016-05-13','2016-05-16','2016-05-17'])
#print(b_dlt)
b_dlt[20:23].T.plot()
a,b = get_return_and_delta(alldata,ma=[20])
print(a['2016-05-17':'2016-06-17'])
