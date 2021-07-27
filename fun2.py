import pandas as pd  
import numpy as np
from scipy import stats
import tushare as ts 
import matplotlib.pyplot as plt
import datetime
import csv

#正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

#浏览市场行情
def all_stock():
    data = ts.get_today_all()
    data.index = data.code
    data = data.sort_index()

    return data

def row_by_code(market,codes):
    market.index = market.code
    info = market.loc[codes]
    return info

def row_by_name(market,tip):
    market.index = market.name
    info = market.loc[tip]
    return info
    
def sort_by_col(market,which_col):
    data = market.sort_values(by=which_col,ascending=False)
    return data

if __name__ == '__main__':
    market = all_stock()
    market.to_csv('./all_stock.csv')
    print(market)
    
    # #按股票代码查看
    # codes = input('Please input the stock code: ')
    # by_code = row_by_code(market,codes)
    # print(by_code)
    #
    # #按股票名查看
    # tip = input('Please input the stock name: ')
    # by_name = row_by_name(market,tip)
    # print(by_name)
    #
    # #按列排序
    # which_col = input('Please input the column name: ')
    # sortby = sort_by_col(market,which_col)
    # print(sortby.head(20))

