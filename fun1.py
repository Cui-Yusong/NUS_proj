import pandas as pd
import numpy as np
from scipy import stats
import tushare as ts
import matplotlib.pyplot as plt
import datetime
import csv
import mplfinance as mpf
from cycler import cycler
import seaborn as sns  # 引入图表美化库
import time

sns.set()  # 激活

# 正常显示画图时出现的中文和负号
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

# 获取当前时间
time_now = datetime.datetime.now().strftime('%Y-%m-%d')


def suit_code_name(code):
    f = open('stock_name.csv', encoding='utf-8')
    reader = csv.DictReader(f)
    for row in reader:
        col = row
        if row['symbol'] == code:
            name = row['name']
            break
    f.close()
    return name


# 浏览个股行情
def get_stock(code, start='2010-01-01', end=time_now, ktype='d', data_type='close', flag=True):
    # 获取历史行情数据
    stock = ts.get_k_data(code=code, start=start, end=end, ktype=ktype, autype='qfq')

    dtime = pd.to_datetime(stock['date'])

    v = (dtime.values - np.datetime64('1970-01-01T08:00:00Z')) / np.timedelta64(1, 'ms')

    stock['date'] = v
    stock = stock.rename(columns={'volume': 'vol'})
    stock = stock.drop('code', axis=1)

    stock_dict = stock.to_dict('index')
    ans = []
    for i in stock_dict.values():
        ans.append(i)

    # stock.index = pd.to_datetime(stock.date)
    # name = suit_code_name(code)
    # if flag:
    #     stock[data_type].plot(figsize=(12,5),marker=".")
    #     if end=='':
    #         end='2021'
    #     plt.title('{}: {}-{} {} Value Chart'.format(name,start[0:4],end[0:4],data_type))
    #     plt.xlabel('date')
    #     plt.ylabel(data_type)
    #     plt.show()
    return ans


def get_k_line(stock, code):
    kwargs = dict(
        type='candle',
        mav=(5, 50, 120, 200),
        volume=True,
        title='\nStock {} Candle_Line'.format(code),
        ylabel='OHLC Candles',
        ylabel_lower='Shares\nTraded Volume',
        figratio=(12, 5),
        figscale=5)
    mc = mpf.make_marketcolors(
        up='red',
        down='green',
        edge='i',
        wick='i',
        volume='in',
    )
    s = mpf.make_mpf_style(
        gridaxis='both',
        gridstyle='-.',
        y_on_right=False,
        marketcolors=mc)
    mpl.rcParams['axes.prop_cycle'] = cycler(
        color=['dodgerblue', 'deeppink', 'navy', 'teal', 'maroon', 'darkorange', 'indigo'])
    mpl.rcParams['lines.linewidth'] = .5

    mpf.plot(stock, **kwargs, style=s, show_nontrading=False)
    plt.show()


# 浏览实时数据
def get_realtime(code):
    stock = ts.get_realtime_quotes(symbols=code)
    # print('The Stock {} RealTime Info: '.format(code))
    stock = stock[
        ['code', 'name', 'pre_close', 'open', 'price', 'bid', 'ask', 'volume', 'amount', 'time', 'high', 'low']]
    a = stock['code'].values[0]
    print(a)
    print(type(a))
    return stock


# 均线分析，基于获得stock信息的基础上
'''def ma(stock,name,start='2010-01-01',end=time_now):
    ma_day = [20,52,252]
    for ma in ma_day:
        column_name = "%s日均线" %(str(ma))
        stock[column_name] =stock["close"].rolling(ma).mean()
    #画出收盘价和均线图
    if end=='':
        end='2021'
    stock.loc[start:][["close","20日均线","52日均线","252日均线"]].plot(figsize=(12,6))
    plt.title('{}: {}-{} Chart'.format(name,start[0:4],end[0:4]))
    plt.xlabel('date')
    plt.show()'''


def profit(stock, code, start='2010-01-01', end=time_now):
    stock["daily yield"] = stock["close"].pct_change()
    stock["daily yield"].loc[start:].plot(figsize=(12, 5), marker=".", color="g")
    plt.xlabel('date')
    plt.ylabel('stock yield')
    if end == '':
        end = '2021'
    plt.title('Stock {}: {}-{} Daily Stock Yield Chart'.format(code, start[0:4], end[0:4]))
    plt.show()


if __name__ == '__main__':
    # stock_code = input('Please input the stock code: ')
    # start_date = input('Please input the start date with the format of "xx-xx-xx": ')
    # end_date = input('Please input the end date with the format of "xx-xx-xx": ')
    # k_type = input('Please input the ktype: ')
    # datatype = input('Please input the col you want to see: ')
    stock_code = '600519'
    start_date = '2021-05-10'
    end_date = '2021-08-10'
    k_type = 'd'
    datatype = 'volume'
    stock_info=get_stock(code=stock_code,start=start_date, end=end_date, ktype=k_type, data_type=datatype)
    # for i in range(50):
    #     stock_real = get_realtime(stock_code)
    #     print(stock_real)
    #     time.sleep(1)
    # pro = ts.pro_api('d22982798d6ecb9bb839fa6b54bafb5d0177f607ab8f39f8ed8eeeda')
    # df = pro.stock_company(ts_code='600519.SH',
    #                        fields='introduction')
    # print(df['introduction'].values[0])
    # stock_k_line = get_k_line(stock_info[0],stock_code)
    # if k_type=='' or k_type=='d' or k_type=='D':
    #     #ma_a = ma(stock_info[0],stock_info[1],start_date,end_date)
    #     pro = profit(stock_info[0],stock_code,start_date,end_date)
    # else:
    #     stock_info2 = get_stock(code=stock_code,start=start_date, end=end_date, data_type=datatype,flag=False)
    #     #ma_a = ma(stock_info2[0],stock_info2[1],start_date,end_date)
    #     pro = profit(stock_info2[0],stock_code,start_date,end_date)
    #
