#-*- coding:UTF-8 -*-
import datetime

import pandas as pd
import sqlalchemy


class ImportOracle():
    def __init__(self):
        self.engine = sqlalchemy.create_engine('oracle://shuzeng:Shuzeng123@10.200.187.161:1521/orcl?charset=utf8')

    def insert(self,add,tablename):
        raise  NotImplementedError

    def fetch(self,sql):
        raise  NotImplementedError


class SQL_(ImportOracle):
    def fetch(self,sql):
        return pd.read_sql(sql,self.engine)

    def to_csv(self,sql):
        df = self.fetch(sql)
        df.to_csv('export.csv')

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

if __name__=='__main__':
    exe = read_csv_excel('/Users/leotao/Downloads/石油ETF回测.csv','择时分析-创')
    print(exe)
    '''
    test = SQL_()
    print('success con')
    sql = 'select * from ALL_INDEX_MONTHLY where code = '+"'"+'sz'+"'"+'order by date_'
    test.to_csv(sql)
    r = mlab.csv2rec('export.csv')
    r.sort()
    '''