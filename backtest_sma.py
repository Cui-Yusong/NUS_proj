from datetime import datetime
import backtrader as bt
import tushare as ts
import pandas as pd
class MyStrategy1(bt.Strategy):
    params=(('maperiod',20),
            ('printlog',False),)
    def __init__(self):
        #指定价格序列
        self.dataclose=self.datas[0].close
        # 初始化交易指令、买卖价格和手续费
        self.order = None
        self.buyprice = None
        self.buycomm = None
        #添加移动均线指标
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.maperiod)
    #策略核心，根据条件执行买卖交易指令（必选）
    def next(self):
        # 记录收盘价
        #self.log(f'收盘价, {dataclose[0]}')
        if self.order: # 检查是否有指令等待执行, 
            return
        # 检查是否持仓   
        if not self.position: # 没有持仓
            #执行买入条件判断：收盘价格上涨突破15日均线
            if self.dataclose[0] > self.sma[0]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                #执行买入
                self.order = self.buy()         
        else:
            #执行卖出条件判断：收盘价格跌破15日均线
            if self.dataclose[0] < self.sma[0]:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                #执行卖出
                self.order = self.sell()
    #交易记录日志（可省略，默认不输出结果）
    def log(self, txt, dt=None,doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()},{txt}')
    #记录交易执行情况（可省略，默认不输出结果）
    def notify_order(self, order):
        # 如果order为submitted/accepted,返回空
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 如果order为buy/sell executed,报告价格结果
        if order.status in [order.Completed]: 
            if order.isbuy():
                self.log(f'买入:\n价格:{order.executed.price},成本:{order.executed.value},手续费:{order.executed.comm}')
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
        self.log(f'策略收益：\n毛收益:{trade.pnl:.2f}, 净收益:{trade.pnlcomm:.2f}')
    #回测结束后输出结果（可省略，默认输出结果）
    def stop(self):
        self.log('(MA均线: %2d日) 期末总资金 %.2f' %(self.params.maperiod, self.broker.getvalue()), doprint=True)

def back(stock_code,startcash):
    # 初始化cerebro回测系统设置
    cerebro = bt.Cerebro()
    # 获取数据

    # start = input('输入回测起始时间(xx-xx-xx)：')
    start = '2018-01-01'
    # end = input('输入回测结束时间(xx-xx-xx)：')
    end = '2021-06-01'

    start1 = datetime.strptime(start, "%Y-%m-%d")
    end1 = datetime.strptime(end, "%Y-%m-%d")

    df = ts.get_k_data(stock_code, autype='qfq', start=start, end=end)
    # df=ts.get_k_data('600000',autype='qfq',start='2018-01-01',end='2021-03-30')
    df.index = pd.to_datetime(df.date)
    df = df[['open', 'high', 'low', 'close', 'volume']]
    data = bt.feeds.PandasData(dataname=df, fromdate=start1, todate=end1)
    # data = bt.feeds.PandasData(dataname=df,fromdate=datetime(2018, 1, 1),todate=datetime(2021, 3, 30))
    # 加载数据
    cerebro.adddata(data)
    # 将交易策略加载到回测系统中
    # 设置printlog=True，表示打印交易日志log
    cerebro.addstrategy(MyStrategy1, maperiod=20, printlog=False)
    # 设置初始资本
    cerebro.broker.setcash(startcash)
    # 设置交易手续费为 0.1%
    cerebro.broker.setcommission(commission=0.001)
    # 设置买入设置、策略、数量
    cerebro.addsizer(bt.sizers.FixedSize, stake=1000)

    # 回测结果
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='_AnnualReturn')
    cerebro.addanalyzer(bt.analyzers.Calmar, _name='_Calmar')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')
    # cerebro.addanalyzer(bt.analyzers.TimeDrawDown, _name='_TimeDrawDown')
    cerebro.addanalyzer(bt.analyzers.GrossLeverage, _name='_GrossLeverage')
    cerebro.addanalyzer(bt.analyzers.PositionsValue, _name='_PositionsValue')
    cerebro.addanalyzer(bt.analyzers.LogReturnsRolling, _name='_LogReturnsRolling')
    cerebro.addanalyzer(bt.analyzers.PeriodStats, _name='_PeriodStats')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='_Returns')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='_SharpeRatio')
    # cerebro.addanalyzer(bt.analyzers.SharpeRatio_A, _name='_SharpeRatio_A')
    cerebro.addanalyzer(bt.analyzers.SQN, _name='_SQN')
    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='_TimeReturn')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='_TradeAnalyzer')
    cerebro.addanalyzer(bt.analyzers.Transactions, _name='_Transactions')
    cerebro.addanalyzer(bt.analyzers.VWR, _name='_VWR')

    results = cerebro.run()
    # 获取最后总资金
    portvalue = cerebro.broker.getvalue()
    fpnl = portvalue - startcash

    performance_dict = {}
    calmar_ratio = list(results[0].analyzers._Calmar.get_analysis().values())[-1]
    drawdown_info = results[0].analyzers._DrawDown.get_analysis()
    average_drawdown_len = drawdown_info['len']
    average_drawdown_rate = drawdown_info['drawdown']
    average_drawdown_money = drawdown_info['moneydown']
    max_drawdown_len = drawdown_info['max']['len']
    max_drawdown_rate = drawdown_info['max']['drawdown']
    max_drawdown_money = drawdown_info['max']['moneydown']
    PeriodStats_info = results[0].analyzers._PeriodStats.get_analysis()
    average_rate = PeriodStats_info['average']
    stddev_rate = PeriodStats_info['stddev']
    positive_year = PeriodStats_info['positive']
    negative_year = PeriodStats_info['negative']
    nochange_year = PeriodStats_info['nochange']
    best_year = PeriodStats_info['best']
    worst_year = PeriodStats_info['worst']
    SQN_info = results[0].analyzers._SQN.get_analysis()
    sqn_ratio = SQN_info['sqn']
    VWR_info = results[0].analyzers._VWR.get_analysis()
    vwr_ratio = VWR_info['vwr']
    sharpe_info = results[0].analyzers._SharpeRatio.get_analysis()
    sharpe_ratio = sharpe_info['sharperatio']

    performance_dict['calmar_ratio'] = calmar_ratio
    performance_dict['average_drawdown_len'] = average_drawdown_len
    performance_dict['average_drawdown_rate'] = average_drawdown_rate
    performance_dict['average_drawdown_money'] = average_drawdown_money
    performance_dict['max_drawdown_len'] = max_drawdown_len
    performance_dict['max_drawdown_rate'] = max_drawdown_rate
    performance_dict['max_drawdown_money'] = max_drawdown_money
    performance_dict['average_rate'] = average_rate
    performance_dict['stddev_rate'] = stddev_rate
    performance_dict['positive_year'] = positive_year
    performance_dict['negative_year'] = negative_year
    performance_dict['nochange_year'] = nochange_year
    performance_dict['best_year'] = best_year
    performance_dict['worst_year'] = worst_year
    performance_dict['sqn_ratio'] = sqn_ratio
    performance_dict['vwr_ratio'] = vwr_ratio
    performance_dict['sharpe_info'] = sharpe_ratio

    performance = pd.DataFrame(performance_dict, index=[0]).T
    print(performance)

    # Print out the final result
    print(f'\n总资金: {portvalue:.2f}')
    print(f'净收益: {round(fpnl, 2)}')

    cerebro.plot(style='candlestick')

if __name__ == '__main__':
    stock_code = input('输入回测股票代码：')
    startcash = float(input('输入回测初始资本：'))
    back(stock_code,startcash)