import pandas as pd  
import numpy as np
from scipy import stats
import tushare as ts 
import matplotlib.pyplot as plt
import datetime
from fun2 import all_stock,sort_by_col

#正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

#获取当前时间
time_now = datetime.datetime.now().strftime('%Y-%m-%d')

def create_stock_pool(info):
    #存储编码
    #settlement为昨日收盘价
    #暂时将昨日收盘价前10位股票加入股票池
    stock_pool = []
    for i in range(0, len(info)):
        temp = info.iloc[i]['code']
        stock_pool.append(temp)
    return stock_pool

if __name__ == '__main__':
    market = all_stock()
    #which_col = input('Please input the column name: ')
    sortby = sort_by_col(market,'settlement').head(10)
    stock_pool = create_stock_pool(sortby)
    print(stock_pool)
