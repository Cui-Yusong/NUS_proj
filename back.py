import math
import sys
import tushare as ts
# sys.path.append("../")
import fun1
import numpy as np
import flask
import json

app = flask.Flask(__name__, static_url_path='')

global code


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
    global code
    # code = int(code)
    stock_dict = {}
    stock = fun1.get_realtime(code)

    pro = ts.pro_api('d22982798d6ecb9bb839fa6b54bafb5d0177f607ab8f39f8ed8eeeda')
    ts_code = str(code) + '.SH'
    company = pro.stock_company(ts_code=ts_code, fields='introduction')
    # print('The Stock {} RealTime Info: '.format(code))
    stock = stock[['code', 'name', 'pre_close', 'open', 'price', 'bid', 'ask', 'volume', 'amount', 'time', 'high', 'low']]
    print(stock['price'].values[0])
    stock_dict['Name'] = stock['name'].values[0]
    stock_dict['intro'] = company['introduction'].values[0]
    # stock_dict['intro'] = 'intro'
    stock_dict['price'] = stock['price'].values[0]
    stock_dict['Previous Close'] = stock['pre_close'].values[0]
    stock_dict['Open'] = stock['open'].values[0]
    stock_dict['Bid'] = stock['bid'].values[0]
    stock_dict['Ask'] = stock['ask'].values[0]
    # stock_dict['Range'] = stock['high']-stock['low'].values[0]
    stock_dict['Range'] = stock['low'].values[0]
    stock_dict['Vol'] = stock['volume'].values[0]
    return json.dumps(stock_dict)


@app.route("/getData", methods=["GET"])
def getdata():
    with open("./data_demo.json",
              "r") as f:
        stock1 = json.load(f, strict=False)
    stock_code = '600519'
    start_date = '2021-05-10'
    end_date = '2021-08-10'
    k_type = 'd'
    datatype = 'volume'
    stock2 = fun1.get_stock(code=stock_code, start=start_date, end=end_date, ktype=k_type, data_type='close', flag=True)

    return json.dumps(stock2)


if __name__ == "__main__":
    app.run(debug=True, port=5007)
