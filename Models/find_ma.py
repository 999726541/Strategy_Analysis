#-*- coding:UTF-8 -*-
import datetime

import pandas as pd
import tushare as ts


class MA_CALCULATOR():

    def __init__(self,df):
        '''
        Index is the date of data
        :param df:  DataFrame
        '''
        try:
            datetime.datetime.strptime(df.index[0],'%Y-%d-%m')
        except Exception:
            raise 'Index of the DataFrame is not date'
        self._df = df
        self._df = self._df.sort_index()

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
    df = df.reset_index()
    test = MA_CALCULATOR(df)
    df = test.get_ma(ll=[5],column_name='close')
    print(df)