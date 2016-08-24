#-*- coding:UTF-8 -*-
import datetime
import json

import pandas as pd
import tushare as ts
from pymongo import MongoClient

from Models.find_ma import MA_CALCULATOR


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)


    return conn[db]


def read_mongo(db, collection, query=None, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)
    print(cursor)
    # Expand the cursor and construct the DataFrame
    df = []
    for element in cursor:
        # Delete the _id
        if no_id:
            try:
                df.append(pd.DataFrame(element).drop('_id',axis=1))
            except Exception as e:
                raise 'Format of db is not right, plz check the database is {xx:{aaa:bbb}}'
        else:
            try:
                df.append(pd.DataFrame(element))
            except Exception as e:
                raise 'Format of db is not right, plz check the database is {xx:{aaa:bbb}}'
    return df

def write_to_mongo(df,db,collection, host='localhost', port=27017, username=None, password=None,id=None):
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)
    content = json.loads(df.to_json())
    if id != None:
        content['_id'] = id
    db[collection].insert(content)


def read_csv_excel(path,sheetname=None):
    if '.xlsx' in path:
        df = pd.read_excel(path,sheetname=sheetname)
    if '.csv' in path:
        df = pd.read_csv(path)
    #print(df)
    for i in range(len(df)):
        #print(df.date[i])
        #print(str(datetime.datetime.strptime(df.date[k].replace(' ','').replace('-','/'),('%Y/%m/%d')))[0:10])
        df.loc[i,'date'] = str(datetime.datetime.strptime(df.date[i].replace(' ','').replace('-','/'),('%Y/%m/%d')))[0:10]
    #print(df)
    df = df.set_index('date')
    return df


def get_his_data(code, start='2014-01-01', end=str(datetime.datetime.today())[0:10], ma=[5, 12, 13, 18, 20, 30, 60, 120], period='day',
                 column_name='close'):
    df = ts.get_hist_data(code)
    df = MA_CALCULATOR(df)
    df = df.get_ma(ll=ma, period=period, column_name=column_name)
    df = df[start:end]
    if df.isnull().any().any():
        print(df)
        raise 'Need more date info for calculating MA before last NaN'
    return df


def get_his_data_EMA(code, start='2014-12-31', end=str(datetime.datetime.today())[0:10], ema=[5, 12, 13, 18, 20, 30, 60, 120], period='day',
                 column_name='close'):
    df = ts.get_hist_data(code)
    df = MA_CALCULATOR(df)
    df = df.get_ema(ll=ema, period=period, column_name=column_name)
    df = df[start:end]
    if df.isnull().any().any():
        raise 'Need more date info for calculating MA before last NaN'
    return df


def get_his_data_WMA(code, start='2014-12-31', end=str(datetime.datetime.today())[0:10],
                     wma=[5, 12, 13, 18, 20, 30, 60, 120], period='day',
                     column_name='close'):
    df = ts.get_hist_data(code)
    df = MA_CALCULATOR(df)
    df = df.get_wma(ll=wma, period=period, column_name=column_name)
    df = df[start:end]
    if df.isnull().any().any():
        raise 'Need more date info for calculating MA before last NaN'
    return df


if __name__=='__main__':
    exe = read_mongo('testdb','hist')
    for i in exe:
        print(i)
        len(i)
    #exe = ts.get_hist_data('000001')
    #add = write_to_mongo(df=exe,db='testdb',collection='hist',id='000001')
    '''
    test = SQL_()
    print('success con')
    sql = 'select * from ALL_INDEX_MONTHLY where code = '+"'"+'sz'+"'"+'order by date_'
    test.to_csv(sql)
    r = mlab.csv2rec('export.csv')
    r.sort()
    '''