from pyalgotrade.tools import yahoofinance
from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import ma
import logging
import tushare as ts
import pandas
import sqlalchemy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.ticker as ticker




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


if __name__=='__main__':
    test = SQL_()
    print('success con')
    sql = 'select * from ALL_INDEX_MONTHLY where code = '+"'"+'sz'+"'"+'order by date_'
    test.to_csv(sql)
    r = mlab.csv2rec('export.csv')
    r.sort()