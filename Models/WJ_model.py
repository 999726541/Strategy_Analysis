import tushare as ts
import csv
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import datetime
from Strategy import Strategy_Base

class COEFF(Strategy_Base):
    def find_date(self,today = str(datetime.date.today()), n = 8,t = 1, period = 'week'):
        if period == 'week':
            #如果周期是周为单位,往后推算n-1周de周一为起始点
            _day = datetime.datetime.strptime(today, '%Y-%m-%d')
            _day = datetime.datetime.strptime(today, '%Y-%m-%d')-datetime.timedelta((n-t-1)*7)
            i = _day.isoweekday()
            _day_last = _day - datetime.timedelta(i-1)
            return str(_day_last)[:10]
        if period == 'month':
            z = int(today[5:7]) - (n - t-1)
            #print(z)
            if z <= 0:
                z = abs(z)
                mon = 12-z%12
                if len(str(mon))==1: mon = '0'+str(mon)
                _day_last = str(int(today[0:4])-1-int(int(z)/12))+'-'+str(mon)+'-'+'01'
            else:
                if len(str(z)) == 1: z = '0' + str(z)
                _day_last = str(int(today[0:4]) - int(int(z) / 12)) + '-' + str(z) + '-' + '01'
            return _day_last
        else:
            raise 'period is not right'

    def find_a(self,n=8,t=1,today = str(datetime.date.today()),code = None,period = 'week'):
        info = ts.get_hist_data(code, self.find_date(today=today,n=n,t=t,period=period), today)
        print(info)
        _min = min(info[i:i + 1].low[0] for i in range(len(info)))
        return _min

    def find_b(self,n=8,t=1,today = str(datetime.date.today()),code = None,period = 'week'):
        info = ts.get_hist_data(code, self.find_date(today=today, n=n, t=t, period=period), today)
        print(info)
        _max = max(info[i:i + 1].high[0] for i in range(len(info)))
        return _max

    def find_c(self,a,b,today = str(datetime.date.today()),code = None):
        info = ts.get_hist_data(code, today, today)
        #print(info)
        close = round(info[0:1].close[0],3)
        #print(close)
        return (close - a)/(a-b)*100




if __name__=='__main__':
    test = COEFF()
    #print(test.find_b(today='2016-06-27',period='month',code = 'sz',n=2))
    print(test.find_c(1,2,code='sz'))
