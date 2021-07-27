import math
import sys
import tushare as ts
# sys.path.append("../")
import fun1
import numpy as np
import flask
import json
import backtest_sma
import random
import fun2

app = flask.Flask(__name__, static_url_path='')

global code
global price

@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/query")
def index2():
    return flask.render_template("test.html")


@app.route("/makequery", methods=["GET"])
def getquery():
    global code
    code = flask.request.args.get("code")
    # year = int(tmp_date[:4])
    # print(code)
    stock_dict = {}
    stock_dict['Name'] = code
    return json.dumps(stock_dict)


@app.route("/getPrice", methods=["GET"])
def getPrice():
    global code,price
    # code = int(code)
    stock_dict = {}
    stock = fun1.get_realtime(code)

    pro = ts.pro_api('d22982798d6ecb9bb839fa6b54bafb5d0177f607ab8f39f8ed8eeeda')
    if int(code) > 400000:
        ts_code = str(code) + '.SH'
    else:
        ts_code = str(code) + '.SZ'

    company = pro.stock_company(ts_code=ts_code, fields='introduction')
    # print('The Stock {} RealTime Info: '.format(code))
    stock = stock[
        ['code', 'name', 'pre_close', 'open', 'price', 'bid', 'ask', 'volume', 'amount', 'time', 'high', 'low']]
    print(stock['price'].values[0])
    stock_dict['Name'] = stock['name'].values[0]
    stock_dict['intro'] = company['introduction'].values[0]
    stock_dict['price'] = stock['price'].values[0]
    price = stock['price'].values[0]
    stock_dict['Previous Close'] = stock['pre_close'].values[0]
    stock_dict['Open'] = stock['open'].values[0]
    stock_dict['Bid'] = stock['bid'].values[0]
    stock_dict['Ask'] = stock['ask'].values[0]
    # stock_dict['Range'] = stock['high']-stock['low'].values[0]
    stock_dict['Range'] = stock['low'].values[0]
    stock_dict['Vol'] = stock['volume'].values[0]
    return json.dumps(stock_dict)


@app.route("/getData_grid", methods=["GET"])
def getData_grid():
    stocks = fun2.all_stock()
    # stocks = {}
    # for i in range(5):
    #     item = {
    #         'code': i,
    #         'name': 'name',
    #         'open': 500,
    #         'close': 400,
    #         'high': 300,
    #         'low': 200,
    #         'amount': 100,
    #         'change': 'temp',
    #         'history': [j for j in range(25)],
    #         'rating': 2,
    #     }
    #     stocks[i] = item
    # ans = {}
    # ans['ans'] = stocks
    return json.dumps(stocks)


@app.route("/getData", methods=["GET"])
def getdata():
    global code
    stock_code = code
    start_date = '2021-05-10'
    end_date = '2021-08-10'
    k_type = 'd'
    datatype = 'volume'
    stock2 = fun1.get_stock(code=stock_code, start=start_date, end=end_date, ktype=k_type, data_type='close', flag=True)
    return json.dumps(stock2)


@app.route("/backtest", methods=["GET"])
def backtest():
    global code
    money = flask.request.args.get("money")
    ans = backtest_sma.back(code, int(money))
    return json.dumps(ans)


@app.route("/predict", methods=["GET"])
def predict():
    global code,price
    ans = {}
    price = float(price)
    price = int(price)
    pri_range = int(price/20)
    pre_str = "The stock price forecasts for the next 5 days are as follows: "
    ans[0] = pre_str

    for i in range(5):
        tmp = str(i+1)+" day later, the price is ￥"
        pre = int(price) + random.randint(-pri_range,pri_range)
        tmp += str(pre)
        ans[i+1] = tmp
    return json.dumps(ans)


if __name__ == "__main__":
    app.run(debug=True, port=5007)
