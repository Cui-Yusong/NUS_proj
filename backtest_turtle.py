from __future__ import (absolute_import, division, print_function,unicode_literals)
import backtrader as bt
import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
from datetime import datetime

from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

def get_data(code,start='2010-01-01',end='2021-07-01'):
    df=ts.get_k_data(code,autype='qfq',start=start,end=end)
    df.index=pd.to_datetime(df.date)
    df['openinterest']=0
    df=df[['open','high','low','close','volume','openinterest']]
    return df

class TurtleStrategy(bt.Strategy):
    #默认参数
    params = (('long_period',20),('short_period',10),('printlog', False), )   

    def __init__(self):        
        self.order = None      
        self.buyprice = 0      
        self.buycomm = 0      
        self.buy_size = 0      
        self.buy_count = 0       
        # 海龟交易法则中的唐奇安通道和平均波幅ATR        
        self.H_line = bt.indicators.Highest(self.data.high(-1), period=self.p.long_period)        
        self.L_line = bt.indicators.Lowest(self.data.low(-1), period=self.p.short_period)       
        self.TR = bt.indicators.Max((self.data.high(0)- self.data.low(0)),\
                                    abs(self.data.close(-1)-self.data.high(0)), \
                                    abs(self.data.close(-1)  - self.data.low(0)))        
        self.ATR = bt.indicators.SimpleMovingAverage(self.TR, period=14)       
        # 价格与上下轨线的交叉      
        self.buy_signal = bt.ind.CrossOver(self.data.close(0), self.H_line)        
        self.sell_signal = bt.ind.CrossOver(self.data.close(0), self.L_line)    

    def next(self): 
        if self.order:
            return        
        #入场：价格突破上轨线且空仓时        
        if self.buy_signal > 0 and self.buy_count == 0:                                 
            self.buy_size = self.broker.getvalue() * 0.01 / self.ATR            
            self.buy_size  = int(self.buy_size  / 100) * 100                             
            self.sizer.p.stake = self.buy_size             
            self.buy_count = 1            
            self.order = self.buy()
        #加仓：价格上涨了买入价的0.5的ATR且加仓次数少于3次（含）        
        elif self.data.close >self.buyprice+0.5*self.ATR[0] and self.buy_count > 0 and self.buy_count <=4:           
            self.buy_size  = self.broker.getvalue() * 0.01 / self.ATR            
            self.buy_size  = int(self.buy_size  / 100) * 100            
            self.sizer.p.stake = self.buy_size             
            self.order = self.buy()           
            self.buy_count += 1
        #离场：价格跌破下轨线且持仓时        
        elif self.sell_signal < 0 and self.buy_count > 0:            
            self.order = self.sell()            
            self.buy_count = 0
        #止损：价格跌破买入价的2个ATR且持仓时        
        elif self.data.close < (self.buyprice - 2*self.ATR[0]) and self.buy_count > 0:           
            self.order = self.sell()
            self.buy_count = 0

    #交易记录日志（默认不打印结果）
    def log(self, txt, dt=None,doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()},{txt}')

    #记录交易执行情况（默认不输出结果）
    def notify_order(self, order):
        # 如果order为submitted/accepted,返回空
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 如果order为buy/sell executed,报告价格结果
        if order.status in [order.Completed]: 
            if order.isbuy():
                self.log(f'买入:\n价格:{order.executed.price},\
                成本:{order.executed.value},\
                手续费:{order.executed.comm}')

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(f'卖出:\n价格：{order.executed.price},\
                成本: {order.executed.value},\
                手续费{order.executed.comm}')

            self.bar_executed = len(self) 

        # 如果指令取消/交易失败, 报告结果
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('交易失败')
        self.order = None

    #记录交易收益情况（可省略，默认不输出结果）
    def notify_trade(self,trade):
        if not trade.isclosed:
            return
        self.log(f'策略收益：\n毛收益 {trade.pnl:.2f}, 净收益 {trade.pnlcomm:.2f}')

class TradeSizer(bt.Sizer):
    params = (('stake', 1),)    
    def _getsizing(self, comminfo, cash, data, isbuy):        
        if isbuy:          
            return self.p.stake        
        position = self.broker.getposition(data)        
        if not position.size:            
            return 0        
        else:            
            return position.size        
        return self.p.stake

def plot_stock(code,title,start,end):
    dd=ts.get_k_data(code,autype='qfq',start=start,end=end)
    dd.index=pd.to_datetime(dd.date)
    dd.close.plot(figsize=(14,6),color='r')
    plt.title(title+'价格走势\n'+start+':'+end,size=15)
    plt.annotate(f'期间累计涨幅:{(dd.close[-1]/dd.close[0]-1)*100:.2f}%', xy=(dd.index[-150],dd.close.mean()), 
             xytext=(dd.index[-500],dd.close.min()), bbox = dict(boxstyle = 'round,pad=0.5',
            fc = 'yellow', alpha = 0.5),
             arrowprops=dict(facecolor='green', shrink=0.05),fontsize=12)
    plt.show()

def main(code,long_list,short_list,start,end='',startcash=1000000,com=0.001):
    #创建主控制器
    cerebro = bt.Cerebro()      
    #导入策略参数寻优
    #cerebro.optstrategy(TurtleStrategy,long_period=long_list,short_period=short_list)    
    #获取数据
    df = get_data(code,start=start,end=end)
    #将数据加载至回测系统
    data = bt.feeds.PandasData(dataname=df,fromdate=datetime.strptime(start, "%Y-%m-%d"),todate=datetime.strptime(end, "%Y-%m-%d"))    
    cerebro.adddata(data)
    # 将交易策略加载到回测系统中
    cerebro.addstrategy(TurtleStrategy)
    #broker设置资金、手续费
    cerebro.broker.setcash(startcash)           
    cerebro.broker.setcommission(commission=com)    
    #设置买入设置，策略，数量
    cerebro.addsizer(TradeSizer)    

    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='_AnnualReturn')
    cerebro.addanalyzer(bt.analyzers.Calmar, _name='_Calmar')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')
    cerebro.addanalyzer(bt.analyzers.GrossLeverage, _name='_GrossLeverage')
    cerebro.addanalyzer(bt.analyzers.PositionsValue, _name='_PositionsValue')
    cerebro.addanalyzer(bt.analyzers.LogReturnsRolling, _name='_LogReturnsRolling')
    cerebro.addanalyzer(bt.analyzers.PeriodStats, _name='_PeriodStats')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='_Returns')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='_SharpeRatio')
    cerebro.addanalyzer(bt.analyzers.SQN, _name='_SQN')
    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='_TimeReturn')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='_TradeAnalyzer')
    cerebro.addanalyzer(bt.analyzers.Transactions, _name='_Transactions')
    cerebro.addanalyzer(bt.analyzers.VWR, _name='_VWR')

    results = cerebro.run(maxcpus=1)

    performance_dict={}
    calmar_ratio=list(results[0].analyzers._Calmar.get_analysis().values())[-1]
    drawdown_info=results[0].analyzers._DrawDown.get_analysis()
    average_drawdown_len=drawdown_info['len']
    average_drawdown_rate=drawdown_info['drawdown']
    average_drawdown_money=drawdown_info['moneydown']
    max_drawdown_len=drawdown_info['max']['len']
    max_drawdown_rate=drawdown_info['max']['drawdown']
    max_drawdown_money=drawdown_info['max']['moneydown']
    PeriodStats_info=results[0].analyzers._PeriodStats.get_analysis()
    average_rate=PeriodStats_info['average']
    stddev_rate=PeriodStats_info['stddev']
    positive_year=PeriodStats_info['positive']
    negative_year=PeriodStats_info['negative']
    nochange_year=PeriodStats_info['nochange']
    best_year=PeriodStats_info['best']
    worst_year=PeriodStats_info['worst']
    SQN_info=results[0].analyzers._SQN.get_analysis()
    sqn_ratio=SQN_info['sqn']
    VWR_info=results[0].analyzers._VWR.get_analysis()
    vwr_ratio=VWR_info['vwr']
    sharpe_info=results[0].analyzers._SharpeRatio.get_analysis()
    sharpe_ratio=sharpe_info['sharperatio']

    performance_dict['calmar_ratio']=calmar_ratio
    performance_dict['average_drawdown_len']=average_drawdown_len
    performance_dict['average_drawdown_rate']=average_drawdown_rate
    performance_dict['average_drawdown_money']=average_drawdown_money
    performance_dict['max_drawdown_len']=max_drawdown_len
    performance_dict['max_drawdown_rate']=max_drawdown_rate
    performance_dict['max_drawdown_money']=max_drawdown_money
    performance_dict['average_rate']=average_rate
    performance_dict['stddev_rate']=stddev_rate
    performance_dict['positive_year']=positive_year
    performance_dict['negative_year']=negative_year
    performance_dict['nochange_year']=nochange_year
    performance_dict['best_year']=best_year
    performance_dict['worst_year']=worst_year
    performance_dict['sqn_ratio']=sqn_ratio
    performance_dict['vwr_ratio']=vwr_ratio
    performance_dict['sharpe_info']=sharpe_ratio

    performance=pd.DataFrame(performance_dict,index=[0]).T
    print(performance)
    
    portvalue = cerebro.broker.getvalue()
    fpnl = portvalue - startcash
    print(f'\n总资金: {portvalue:.2f}')
    print(f'净收益: {round(fpnl,2)}')

    cerebro.plot(style='candlestick')

stock_code=input('输入回测股票代码：')
start = input('输入回测起始时间(xx-xx-xx)：')
end = input('输入回测结束时间(xx-xx-xx)：')
startcash = float(input('输入回测初始资本：'))
main(stock_code,60,15,start,end,startcash=startcash)
