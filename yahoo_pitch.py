import time

import numpy as np
import pandas as pd
from yahoo_finance import Share

from pitcher import MONGODB


def get_data(stock,start,end):
    data = Share(stock)
    try:
        data = pd.DataFrame(data.get_historical(start_date=start,end_date=end))
    except Exception as e:
        f = open('log.txt',mode='a')
        f.write(stock+'\n')
        f.write(str(e)+'\n')
        return pd.DataFrame()

    try:
        data.index = data.Date
    except Exception as e:
        f = open('log.txt', mode='a')
        f.write(stock+'\n')
        f.write(str(e)+'\n')
        return pd.DataFrame()

    data = data.drop(['Date','Symbol'],axis=1)
    data = data.sort()
    for i in data.columns:
        data[i] = data[i].astype(np.float)
    #data['Adj_Open'] = 0
    #data['Adj_High'] = 0
    #data['Adj_Low'] = 0
    #for i in range(len(data)):
    #    k = data['Adj_Close'][i] / data['Close'][i]
    #    data.loc[i:i+1,'Adj_Open'] = k*data['Open'][i]
    #    data.loc[i:i + 1, 'Adj_High'] = k * data['High'][i]
    #    data.loc[i:i + 1, 'Adj_Low'] = k * data['Low'][i]
    data['Symbol'] = stock
    return data

if __name__=='__main__':
    company_list = pd.read_csv('/Users/leotao/Downloads/companylist.csv')
    company_list = company_list[company_list.loc[company_list['Symbol']=='OFIX'].index[0]:]  # 从特定断点开始
    # print(get_data(company_list.Symbol[0],start='2016-01-01',end='2016-09-09'))
    mongo = MONGODB(db='NASDAQ_ALL')    # 打开端口
    ii = 0
    for code in company_list.Symbol:    # 所有NASDAQ股票
        print('Process : '+code)
        data = get_data(code,start='2012-01-01',end='2016-09-09')
        if len(data) == 0: continue
        try:
            mongo.write_to_mongo(data,collection='until_2016-09-09',id=code)    # 输入数据
        except Exception as e:
            f = open('log.txt', mode='a')
            f.write(code + '\n')
            f.write(str(e) + '\n')
            continue
        if ii ==300:    # 防止反爬虫切断
            time.sleep(600)
            ii=0
        ii += 1