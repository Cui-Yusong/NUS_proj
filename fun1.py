import pandas as pd  
import numpy as np
from scipy import stats
import tushare as ts 
import matplotlib.pyplot as plt
import datetime
import csv
import mplfinance as mpf
from cycler import cycler
import seaborn as sns  #引入图表美化库
sns.set()#激活


#正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

#获取当前时间
time_now = datetime.datetime.now().strftime('%Y-%m-%d')

def suit_code_name(code):
    f = open('stock_name.csv',encoding='utf-8')
    reader = csv.DictReader(f)
    for row in reader :
        col = row
        if row['symbol']==code:
            name = row['name']
            break
    f.close()
    return name

#浏览个股行情
def get_stock(code, start='2010-01-01', end=time_now, ktype='d',data_type='close',flag=True):
    #获取历史行情数据
    stock = ts.get_k_data(code=code,start=start,end=end,ktype=ktype,autype='qfq')
    print(stock)
    stock.index = pd.to_datetime(stock.date)
    name = suit_code_name(code)
    if flag:
        stock[data_type].plot(figsize=(12,5),marker=".")
        if end=='':
            end='2021'
        plt.title('{}: {}-{} {} Value Chart'.format(name,start[0:4],end[0:4],data_type))
        plt.xlabel('date')
        plt.ylabel(data_type)
        plt.show()
    return stock,name

def get_k_line(stock,code):
    kwargs = dict(
        type='candle', 
        mav=(5, 50, 120,200), 
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
    mpl.rcParams['axes.prop_cycle'] = cycler(color=['dodgerblue', 'deeppink', 'navy', 'teal', 'maroon', 'darkorange', 'indigo'])
    mpl.rcParams['lines.linewidth'] = .5

    mpf.plot(stock, **kwargs, style=s, show_nontrading=False)
    plt.show()
    

#浏览实时数据
def get_realtime(code):
    stock = ts.get_realtime_quotes(symbols=code)
    print('The Stock {} RealTime Info: '.format(code))
    stock = stock[['code','name','pre_close','open','price','bid','ask','volume','amount','date','time']]
    print(stock)

#均线分析，基于获得stock信息的基础上
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

def profit(stock,code,start='2010-01-01',end=time_now):
    stock["daily yield"] = stock["close"].pct_change()
    stock["daily yield"].loc[start:].plot(figsize=(12,5),marker=".",color="g")
    plt.xlabel('date')
    plt.ylabel('stock yield')
    if end=='':
        end='2021'
    plt.title('Stock {}: {}-{} Daily Stock Yield Chart'.format(code,start[0:4],end[0:4]))
    plt.show()
    
if __name__ == '__main__':
    stock_code = input('Please input the stock code: ')
    start_date = input('Please input the start date with the format of "xx-xx-xx": ')
    end_date = input('Please input the end date with the format of "xx-xx-xx": ')
    k_type = input('Please input the ktype: ')
    datatype = input('Please input the col you want to see: ')
    stock_info=get_stock(code=stock_code,start=start_date, end=end_date, ktype=k_type, data_type=datatype)
    stock_real = get_realtime(stock_code)
    stock_k_line = get_k_line(stock_info[0],stock_code)
    if k_type=='' or k_type=='d' or k_type=='D':
        #ma_a = ma(stock_info[0],stock_info[1],start_date,end_date)
        pro = profit(stock_info[0],stock_code,start_date,end_date)
    else:
        stock_info2 = get_stock(code=stock_code,start=start_date, end=end_date, data_type=datatype,flag=False)
        #ma_a = ma(stock_info2[0],stock_info2[1],start_date,end_date)
        pro = profit(stock_info2[0],stock_code,start_date,end_date)
    
