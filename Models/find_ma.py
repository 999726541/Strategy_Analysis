#-*- coding:UTF-8 -*-
import tushare as ts
import csv
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import datetime


class MA_CALCULATOR():

    def __init__(self,df):
        '''
        :param df:  DataFrame
        '''
        self._df = df

    def find_date(self, dealy, today):
        _day = datetime.datetime.strptime(today, '%Y-%m-%d') - datetime.timedelta(dealy)
        return str(_day)[:10]

    def __ma(self, n=7, period='day', column_name='close'):
        if period == 'day':
            if len(self._df) < n: raise str('No enough data to calculate MA')
            # df = pd.rolling_mean(self.__df['close'], n)
            df = self._df['close'].rolling(n).mean()
            name = 'ma_' + str(n) + '_' + column_name
            df.name = name
            self._df = pd.concat([self._df, df], axis=1)
            print('calculated: ' + 'ma_' + str(n) + '_' + column_name + ' success')

    def get_ma(self, ll=[5, 12, 13, 18, 20, 30, 60, 120], period='day', column_name='close'):
        '''
        :param ll: list
        :param period:
        :param column_name:
        :return:
        '''
        for i in ll:
            self.__ma(n=i, period=period, column_name=column_name)
        return self._df


if __name__=='__main__':
    df = ts.get_hist_data('hs300')
    test = MA_CALCULATOR(df)
    df = test.get_ma(ll=[7],column_name='close')
    print(df)