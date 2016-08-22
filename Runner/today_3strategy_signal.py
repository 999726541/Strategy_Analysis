#-*-coding:UTF-8-*-
import datetime

from Models.Closed_Price_Prediction_model import arbitrary_prediction
from Strategys.INDEX_STRATEGY.CYB import CYB
from Strategys.INDEX_STRATEGY.Gold_ETF import GOLD_ETF
from Strategys.INDEX_STRATEGY.NSDK import NSDK
from Strategys.INDEX_STRATEGY.hs_300_strategy import hs_300_strategy
from Strategys.INDEX_STRATEGY.petro_ETF import PETRO_ETF
from pitcher import get_his_data

today = datetime.datetime.today()-datetime.timedelta(1)
yesterday = str(today)[0:10]
def tree_predict(df):
    xx = arbitrary_prediction(df)
    return [xx.one_day_gradient_change()]


gold_index = get_his_data('159934',ma=[4,5,12,13,16,18,20,30,60,120,14])
gold_index = tree_predict(gold_index)




petro_index = get_his_data('162411',ma=[4,5,12,13,16,18,20,30,60,120,14])
petro_index = tree_predict(petro_index)



hs300_index = get_his_data('hs300',ma = [5,12,13,16,18,20,30,60,120,14])
hs300_index = tree_predict(hs300_index)



cyb = get_his_data('cyb',ma = [4,5,12,13,16,18,20,30,60,120,14,10])
cyb = tree_predict(cyb)


NSD_ETF = get_his_data('513100',ma=[3,60,120,250])
NSD_ETF = tree_predict(NSD_ETF)


open('todays_results.csv','w')
print('Processing Gold_Index')
open('todays_results.csv', 'a').write('GOLD_Prediction')
for i in gold_index:
    gold = GOLD_ETF(i)
    gold = gold.today_signal()
    gold.to_csv('todays_results.csv',mode='a')
    open('todays_results.csv', 'a').write('\n')
open('todays_results.csv','a').write('\n')



print('Processing Petro_index')
open('todays_results.csv', 'a').write('OIL_Prediction')
for i in petro_index:
    gold = PETRO_ETF(i)
    gold = gold.today_signal()
    gold.to_csv('todays_results.csv',mode='a')
    open('todays_results.csv', 'a').write('\n')
open('todays_results.csv','a').write('\n')


print('Processing hs300_index')
open('todays_results.csv', 'a').write('hs300_Prediction')
for i in hs300_index:
    gold = hs_300_strategy(i)
    gold = gold.today_signal()
    gold.to_csv('todays_results.csv',mode='a')
    open('todays_results.csv', 'a').write('\n')
open('todays_results.csv','a').write('\n')


print('Processing cyb')
open('todays_results.csv', 'a').write('CYB_prediction')
for i in cyb:
    gold = CYB(i)
    gold = gold.today_signal()
    gold.to_csv('todays_results.csv',mode='a')
    open('todays_results.csv', 'a').write('\n')
open('todays_results.csv','a').write('\n')

print('Processing NSD_index')
open('todays_results.csv', 'a').write('NASDAQ_Prediction')
for i in NSD_ETF:
    gold = NSDK(i)
    gold = gold.today_signal()
    gold.to_csv('todays_results.csv',mode='a')
    open('todays_results.csv', 'a').write('\n')
open('todays_results.csv','a').write('\n')


#print('黄金今日买卖信号: ')
#gold.today_signal()
#print('石油今日买卖信号: ')
#petro.today_signal()
#print('沪深300今日买卖信号: ')
#hs300#.today_signal()
#print('创业板今日买卖信号: ')
#cyb.today_signal()
