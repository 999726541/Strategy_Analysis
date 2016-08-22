# -*- coding:utf-8 -*-

import datetime

import pandas as pd

from pitcher import read_mongo


def sort_df_index(df):
    #reset index
    df = df.reset_index()
    df['index'] = df['index'].apply(int)
    df = df.set_index('index').sort_index()
    return df


alldata = read_mongo(db='MA_testback', collection='Single_MA_rolling')
length = len(alldata)
zz = pd.DataFrame()
dayy = '2015-01-01'
for i in range(10):
    df = read_mongo(db='MA_testback', collection='Single_MA_rolling',query={'_id':dayy})
    print(df[0])
    date = df[0]['start'][0]
    df = pd.DataFrame(df[0][['return']])
    name = 'return_'+str(date)
    df = df.rename(columns={'return':name})
    zz = pd.concat([zz,sort_df_index(df)],axis=1)
    dayy = str(datetime.datetime.strptime(dayy,'%Y-%m-%d')+datetime.timedelta(1))[:10]
print(zz)