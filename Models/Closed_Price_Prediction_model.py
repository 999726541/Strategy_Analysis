#-*-coding:UTF-8-*-
import datetime

import pandas as pd
import tushare as ts


class arbitrary_prediction():
    def __init__(self,df):
        self._df = df
        self._last_price = self._df.close[len(self._df)-1]
        self._last_date = datetime.datetime.strptime(self._df.index[-1:][0],'%Y-%m-%d')

    def ten_pct_up(self,up=0.1,predict_days=3):
        dic = {}
        dic['date'] = [str(self._last_date + datetime.timedelta(i+1))[:10] for i in range(predict_days)]
        dic['close'] = [self._last_price*(1+up)]*predict_days
        _df = pd.DataFrame(dic)
        _df = _df.set_index('date')
        _df = pd.concat([self._df,_df])
        return _df

    def ten_pct_down(self, down=0.1, predict_days=3):
        dic = {}
        dic['date'] = [str(self._last_date + datetime.timedelta(i + 1))[:10] for i in range(predict_days)]
        dic['close'] = [self._last_price * (1 - down)] * predict_days
        _df = pd.DataFrame(dic)
        _df = _df.set_index('date')
        _df = pd.concat([self._df, _df])
        return _df

    def ten_pct_remain(self, predict_days=3):
        dic = {}
        dic['date'] = [str(self._last_date + datetime.timedelta(i + 1))[:10] for i in range(predict_days)]
        dic['close'] = [self._last_price ] * predict_days
        _df = pd.DataFrame(dic)
        _df = _df.set_index('date')
        _df = pd.concat([self._df, _df])
        return _df

    def one_day_gradient_change(self,predict_days = 3):
        gradient = self._last_price - self._df.close[len(self._df)-2]
        dic = {}
        dic['date'] = [str(self._last_date + datetime.timedelta(i + 1))[:10] for i in range(predict_days)]
        dic['close'] = []
        for i in range(predict_days):
            dic['close'].append(self._last_price+(i+1)*gradient)
        _df = pd.DataFrame(dic)
        _df = _df.set_index('date')
        _df = pd.concat([self._df, _df])
        return _df


if __name__=='__main__':
    df = ts.get_hist_data('000001','2016-08-08')
    df = arbitrary_prediction(df)
    print(df.ten_pct_up())
    print(df.ten_pct_down())
    print(df.ten_pct_remain())
    print(df.one_day_gradient_change())
