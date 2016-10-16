import itertools
import math

import pandas as pd
import pylab

from Models.sta_arb import Sta_arb_draw,find_cointegrated_values
from pitcher import MONGODB
from yahoo_pitch import get_data as get_yahoo


def get_company_list():
    company_list = pd.read_csv('/Users/leotao/PycharmProjects/Strategy_Analysis/Models/companylist.csv')
    company_list = pd.concat([company_list['Symbol'],company_list['Sector']],axis=1).sort_values(by='Sector')   # 返回一个companylist和sector
    return company_list


def get_data(list_name,collection):
    assert type(list_name) is list
    all_data=[]
    con = MONGODB(db='NASDAQ_ALL')
    for i in list_name:
        data = con.read_mongo(collection=collection,query={'_id':i})
        if len(data)==0:continue
        all_data.append(data[0])
    return all_data


def get_all(collection):
    con = MONGODB(db='NASDAQ_ALL')
    data = con.read_mongo(collection=collection)
    print('fetch total #df :' + str(len(data)))
    return data



def data_date_match(df1,df2,start,end,parameter):   # 返回一个整理好的x*2的DF
    df1 = df1[start:end]
    df2 = df2[start:end]
    if len(df1) < 30 or len(df2) < 30: return pd.DataFrame()
    df = pd.concat([df1[parameter],df2[parameter]],axis=1)
    df.columns = [df1.Symbol[0],df2.Symbol[0]]
    df = df.dropna()
    return df


def corrcof_write(df_list,startdate,enddate,ff,numbers='0-300'):
    assert type(df_list) is list
    length = len(df_list)
    combination = list(itertools.combinations(range(length), 2))
    con = MONGODB(db='NASDAQ_CORRELATION')
    i=0
    for comb in combination:
        a = comb[0]
        b = comb[1]
        data = data_date_match(df_list[a], df_list[b], start=startdate, end=enddate, parameter='Adj_Close')
        #print(data)
        data = data.pct_change().dropna()
        #print(data)
        if len(data)==0:continue
        name = data.columns#
        print('Process '+ name[0]+'_'+name[1])
        ff.write(str(name[0]) + ',' + str(name[1]) + ',' + str(data.corr('pearson')[name[0]][1]) +
                ',' + data.index[0:1][0] + ',' + data.index[-1:][0] + '\n')
    #
        #df = pd.DataFrame({'Correlation':[data.corr('pearson')[name[0]][1]],
        #                   'start_date':[startdate],'end_date':[enddate]})
        #con.write_to_mongo(df,collection=numbers,id=name[0]+'_'+name[1])




# Personnal setting envolved,Executive part
def calculate_range(start,end):
    all_name = get_company_list()
    q = list(all_name['Symbol'])[start:end]
    return get_data(q,'until_2016-09-09')


def draw_pairs(a,b,startdate='2015-05-01',enddate='2016-05-01', data = 'Adj_Close'):
    con = MONGODB(db='NASDAQ_ALL')
    a = con.read_mongo(collection='until_2016-09-09', query={'_id': a})[0]
    b = con.read_mongo(collection='until_2016-09-09', query={'_id': b})[0]
    graph = data_date_match(a,b,start=startdate,end=enddate,parameter=data)
    graph.plot()
    pylab.show()
    ratio = sum(graph[list(graph.columns)[0]])/sum(graph[list(graph.columns)[1]])
    rratio = 1/ratio-1
    rratio = math.ceil(rratio)
    ratio = math.ceil(ratio)
    ll = graph[list(graph.columns)[0]]*rratio-graph[list(graph.columns)[1]]*ratio
    print(ratio,rratio)
    ll.plot()
    pylab.show()

def every_day_check(date):
    mongo = MONGODB(db='NASDAQ_CORRELATION')
    #f = open('results.csv', mode='a')
    #data = pd.read_csv('/Users/leotao/Downloads/correlation_list_1.csv')
    #data.columns = ['code1', 'code2', 'correlation', 'start', 'end']
    #result = data.loc[data['correlation'] >= 0.98]
    result = mongo.read_mongo(collection='2015-05-01/2016-05-01',query={'_id':'range: 0.94_0.95'})
    result = result[0]
    code1 = list(result['code1'])
    code2 = list(result['code2'])
    for n in range(len(result)):
        stock1 = code1[n]
        stock2 = code2[n]
        print(stock1, stock2)
        a = get_yahoo(stock1, start='2016-01-01', end=date)
        b = get_yahoo(stock2, start='2016-01-01', end=date)
        dataa = data_date_match(a, b, '2016-01-01', date, parameter='Adj_Close')
        coin = find_cointegrated_values(dataa)
        if coin <= 0.05:
            test = Sta_arb_draw(dataa)
            df = test.signal_today()
            df.to_csv('results.csv',mode='a',header=False,index=False)


def check_pair(stock1,stock2,start,date):
    a = get_yahoo(stock1, start=start, end=date)
    b = get_yahoo(stock2, start=start, end=date)
    dd = data_date_match(a, b, start, date, parameter='Adj_Close')
    #print(dd.corr())
    #dd = dd.pct_change().dropna()
    test = Sta_arb_draw(dd)  #
    test.get_summary_parameter()
    test.draw_OLS()
    test.draw_result()
    test.signal_today()


if __name__=='__main__':
    #ff = open('correlation_list_1.csv', mode='a')
    #corrcof_write(get_all('until_2016-09-09'), startdate='2015-09-09', enddate='2016-09-09',ff=ff,numbers='0-300')
    #draw_pairs('FNK','FAB',startdate='2013-05-01',enddate='2016-09-15')

    #every_day_check('2016-09-26')
    check_pair('CNFR','BV',start='2016-01-01',date='2016-09-27')

    #datas = get_data(['AXAS','AREX'],'until_2016-09-09')
    #a = datas[0]
    #b = datas[1]



    #data = pd.read_csv('/Users/leotao/PycharmProjects/Strategy_Analysis/Models/correlation_list_1.csv',header=None)
    #data.columns = ['code1', 'code2', 'correlation', 'start', 'end']
    #import_data = MONGODB(db='NASDAQ_CORRELATION')
    #print('process')
    #for i in range(-100,100):
    #    k=i+1
    #    a,b = i/100,k/100
    #    print(a, b)
    #    result = data.loc[(data['correlation'] >= a)&(data['correlation'] <= b)]
    #    import_data.write_to_mongo(result,collection='prct_diff/15-09-09_16-09-09',id='range: '+str(i/100)+'_'+str(k/100))


    #import_data.write_to_mongo(data,collection='CORRELATION_VALUE',id='2015-05-01/2016-05-01')
    #results  =  sm.tsa.stattools.coint(d1, d2)
    #print(results[1])
    #print(dd.corr())
    #print(dd.pct_change().corr())
    #dd.pct_change().plot()
    #dd = dd.diff()
    #dd = dd.dropna()
    #print(dd)
    #print(dd.corr())
    #dd.plot()
    #pylab.show()
