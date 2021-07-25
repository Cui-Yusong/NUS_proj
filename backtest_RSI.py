from __future__ import (absolute_import, division, print_function, unicode_literals)
import pandas as pd
import backtrader as bt
from datetime import datetime 
import tushare as ts

#当RSI<30时买入，RSI>70时卖出
class MyStrategy2(bt.Strategy):
    params=(('short',30),
            ('long',70),)
    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(
                   self.data.close, period=21)
    def next(self):
        if not self.position:
            if self.rsi < self.params.short:
                self.buy()
        else:
            if self.rsi > self.params.long:
                self.sell()

stock_code=input('输入回测股票代码：')
start = input('输入回测起始时间(xx-xx-xx)：')
end = input('输入回测结束时间(xx-xx-xx)：')
start1 = datetime.strptime(start, "%Y-%m-%d")
end1 = datetime.strptime(end, "%Y-%m-%d")
df=ts.get_k_data(stock_code,autype='qfq',start=start,end=end)

df.index=pd.to_datetime(df.date)
#df['openinterest'] = 0
df=df[['open','high','low','close','volume']]
data = bt.feeds.PandasData(dataname=df,fromdate=start1,todate=end1)
# 初始化cerebro回测系统设置                           
cerebro = bt.Cerebro()  
# 加载数据
cerebro.adddata(data) 
# 将交易策略加载到回测系统中
cerebro.addstrategy(MyStrategy2) 
# 设置初始资本
startcash = float(input('输入回测初始资本：'))
cerebro.broker.setcash(startcash) 
#每次固定交易数量
cerebro.addsizer(bt.sizers.FixedSize, stake=1000) 
#手续费
cerebro.broker.setcommission(commission=0.001)

#回测结果
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

results = cerebro.run()

#获取最后总资金
portvalue = cerebro.broker.getvalue()
fpnl = portvalue - startcash

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

#Print out the final result
print(f'\n总资金: {portvalue:.2f}')
print(f'净收益: {round(fpnl,2)}')

cerebro.plot(style='candlestick')
