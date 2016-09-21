import itertools
import math

import pandas as pd
import pylab

from Models.sta_arb import Sta_arb_draw
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
        if len(data)==0:continue
        name = data.columns#
        print('Process '+ name[0]+'_'+name[1])
        ff.write(str(name[0]) + ',' + str(name[1]) + ',' + str(data.corr('pearson')[name[0]][1]) +
                ',' + startdate + ',' + enddate + '\n')
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


if __name__=='__main__':
    #ff = open('correlation_list_1.csv', mode='a')
    #corrcof_write(get_all('until_2016-09-09'), startdate='2015-05-01', enddate='2016-05-01',ff=ff,numbers='0-300')
    #draw_pairs('FNK','FAB',startdate='2013-05-01',enddate='2016-09-15')
    #corrcof_write(get_data(['PIH','AXDX'],collection='until_2016-09-09'), startdate='2015-05-01', enddate='2016-05-01', ff=ff, numbers='0-300')
    #con = MONGODB(db='NASDAQ_CORRELATION')
    #print(type(con.read_mongo(collection='0-300')))
    #data = pd.read_csv('/Users/leotao/PycharmProjects/Strategy_Analysis/Stocks_Pick/correlation_list_1.csv')
    #data.columns = ['code1','code2','correlation','start','end']
    #result = data.loc[data['correlation']>=0.98]
    #print(result.sort_values('correlation'))


    #datas = get_data(['IXUS','VXUS'],'until_2016-09-09')
    #a = datas[0]
    #b = datas[1]
    a = get_yahoo('ACWX',start='2016-01-01',end='2016-09-20')
    b = get_yahoo('VYMI',start='2016-01-01',end='2016-09-20')
    dd = data_date_match(a,b,'2016-01-01','2016-09-22',parameter='Adj_Close')
    test = Sta_arb_draw(dd)
    test.get_summary_parameter()
    test.draw_OLS()
    test.draw_result()
    test.signal_today()





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
