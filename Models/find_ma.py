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
            datetime.datetime.strptime(df.index[0],'%Y-%m-%d')

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
            df = self._df[column_name].rolling(n).mean()
            name = 'ma_' + str(n) + '_' + column_name
            df.name = name
            self._df = pd.concat([self._df, df], axis=1)
            print('calculated: ' + 'ma_' + str(n) + '_' + column_name + ' success')

    def __ema(self, n=7, period='day', column_name='close'):
        if period == 'day':
            if len(self._df) < n: raise str('No enough data to calculate MA')
            # df = pd.rolling_mean(self.__df['close'], n)
            df = self._df[column_name].ewm(span=n).mean()
            name = 'ema_' + str(n) + '_' + column_name
            df.name = name
            self._df = pd.concat([self._df, df], axis=1)
            print('calculated: ' + 'ema_' + str(n) + '_' + column_name + ' success')

    def __wma(self,n=7, period='day', column_name='close'):
        if period == 'day':
            for i in range(n-1):
                self._df.loc[i:i+1,'wma_'+ str(n) + '_' + column_name]=self._df[column_name][i]
            for i in range(n-1,len(self._df)):
                count = 0
                count_num = 0
                for k in range(n):
                    count += (n-k)*(self._df[column_name][i-k])
                    count_num += (n-k)
                self._df.loc[i:i + 1, 'wma_' + str(n) + '_' + column_name] = count/(count_num)
            print('calculated: ' + 'wma_' + str(n) + '_' + column_name + ' success')



    def get_ma(self, ll=[5, 12, 13, 18, 20, 30, 60, 120], period='day', column_name='close'):
        '''
        :param ll: list
        :param period:
        :param column_name:
        :return:
        '''
        for i in ll:
            self.__ma(n=i, period=period, column_name=column_name)
        #print(self._df)
        self._df = self._df.drop(self._df.index[0:max(ll)])
        return self._df

    def get_ema(self, ll=[5, 12, 13, 18, 20, 30, 60, 120], period='day', column_name='close'):
        for i in ll:
            self.__ema(n=i, period=period, column_name=column_name)
        # print(self._df)
        return self._df

    def get_wma(self, ll=[5, 12, 13, 18, 20, 30, 60, 120], period='day', column_name='close'):
        for i in ll:
            self.__wma(n=i, period=period, column_name=column_name)
        # print(self._df)
        return self._df

if __name__=='__main__':
    df = ts.get_hist_data('hs300')
    df = df.sort_index()
    test = MA_CALCULATOR(df)
    df = test.get_wma(ll=[5],column_name='close')
    print(df)