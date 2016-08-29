# -*- coding:utf-8 -*-
import  pandas as pd
import tushare as ts


class BANKER_PRICE():
    # 查找在过去 N 天之内是否出现了 K 价格为2个相同数字结尾的最高最低价,如出现视为坐庄价格,并且跟随long or short
    def __init__(self):
        self._all_codes = ts.get_stock_basics().index
        self.long_code = []
        self.short_code = []

    def find_long(self,lookback_days=3,total_range = 50):
        # 查找是否在 lookback 时间范围内出现了相同数字结尾的最高价,且在 total_range里面也是最高价,数据为前复权
        for i in self._all_codes:
            print('process code:' + i)
            try:
                # 截取数据,最大截取回溯日期为3年,也就是出现3年内最低价
                data = ts.get_hist_data(i)[0:total_range]
            except Exception as e:
                raise e
            lowest_price = data['low'].min()
            last_days_low = data[:lookback_days]
            if_exist = pd.DataFrame(last_days_low[last_days_low['low'].isin([lowest_price])])
            if len(if_exist) > 0:
                price = '%.2f'%if_exist['low'][0]
                if price[-2:-1] == price[-1:]:
                    print('Long signal --> code:' +i + ' @ price :' + price + ' @ date:' +if_exist[:1].index[0])
                    if_exist['code'] = i
                    self.long_code.append(if_exist)
        return self.long_code

    def find_short(self,lookback_days=3,total_range = 50):
        # 查找是否在 lookback 时间范围内出现了相同数字结尾的最高价,且在 total_range里面也是最高价,数据为前复权
        for i in self._all_codes:
            print('process code:' + i)
            try:
                data = ts.get_hist_data(i)[0:total_range]
            except Exception as e:
                raise e
            highest_price = data['high'].max()
            # 最近N天出现的最高价
            last_days_high = data[:lookback_days]
            if_exist = pd.DataFrame(last_days_high[last_days_high['high'].isin([highest_price])])
            if len(if_exist) > 0:
                price = '%.2f' % if_exist['high'][0]
                if price[-2:-1] == price[-1:]:
                    print('Short signal --> code:' + i + ' @ price :' + price + ' @ date:' + if_exist[:1].index[0])
                    if_exist['code'] = i
                    self.short_code.append(if_exist)
        return self.short_code

if __name__=='__main__':
    test = BANKER_PRICE()
    test = test.find_long(lookback_days=10,total_range=100)

