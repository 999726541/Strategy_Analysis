# -*- coding:UTF-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pylab
import statsmodels.api as sm


# 输入是一DataFrame，每一列是一支股票在每一日的价格


def find_cointegrated_pairs(dataframe):
    #       得到DataFrame长度
    n = dataframe.shape[1]
    # 初始化p值矩阵
    pvalue_matrix = np.ones((n, n))
    #       抽取列的名称
    keys = dataframe.keys()
    # 初始化强协整组
    pairs = []
    #       对于每一个i
    for i in range(n):
        # 对于大于i的j
        for j in range(i+1, n):
            #       获取相应的两只股票的价格Series
            stock1 = dataframe[keys[i]]
            stock2 = dataframe[keys[j]]
            # 分析它们的协整关系
            result = sm.tsa.stattools.coint(stock1, stock2)
            #       取出并记录p值
            pvalue = result[1]
            pvalue_matrix[i, j] = pvalue
            # 如果p值小于0.05
            if pvalue < 0.05:
                #       记录股票对和相应的p值
                pairs.append((keys[i], keys[j], pvalue))
    # 返回结果
    return pvalue_matrix, pairs


def zscore_test(series,data):
    #  long, short or Do nothing
    result = (data - series.mean()) / np.std(series)
    print(series[-10:])
    if result >= 1: return -1
    if result <= -1: return 1
    else: print('No signal occur')
    return 0


class Sta_arb_draw():
    #import df of two stocks that data matched
    def __init__(self,dataframe):
        self._df = dataframe
        keys = self._df.keys()
        self._x = self._df[keys[0]]
        self._y = self._df[keys[1]]
        X = sm.add_constant(self._x)
        self._result = (sm.OLS(self._y, X)).fit()
        # 价格之间的差值
        self._SS = self._y - self._x * self._result.params[1]
        print('cointegration is :'+str(find_cointegrated_pairs(dataframe)[0][0][1]))

    def get_summary_parameter(self):
        print(self._result.summary())
        # return 第一个是beta0, 第二个是beta1,也就是买股票的一个比例
        return self._result.params

    def draw_OLS(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(self._x, self._y, 'o', label="data")
        ax.plot(self._x, self._result.fittedvalues, 'r', label="OLS")
        ax.legend(loc='best')
        pylab.show()

    def draw_result(self):
        self._SS.plot()
        plt.axhline(self._SS.mean(), color="black", linestyle="--")
        plt.axhline(self._SS.mean() + np.std(self._SS), color="red", linestyle="--")
        plt.axhline(self._SS.mean() - np.std(self._SS), color="green", linestyle="--")
        plt.xlabel("Time")
        plt.ylabel("Stationary Series")
        plt.legend(["Stationary Series", "Mean", "Ceiling", "Floor"])
        print(self._y.name + '=' + str(self._result.params[0]) + '+' + str(self._result.params[1]) + '*' + self._x.name)
        pylab.show()

    def signal_today(self):
        # 最接近的日期
        date = self._SS.index[-1:][0]
        data = self._SS[-1:][0]
        print('test date is :'+date)
        signal = zscore_test(self._SS,data)
        if signal == -1: print('short')
        if signal == 1: print('long')
        return signal
