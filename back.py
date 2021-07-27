import math
import sys
import tushare as ts
# sys.path.append("../")
import fun1
import numpy as np
import flask
import json

app = flask.Flask(__name__, static_url_path='')

code = 1

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/query")
def index2():
    return flask.render_template("test.html")

@app.route("/makequery", methods=["GET"])
def getquery():
    code = flask.request.args.get("code")
    # year = int(tmp_date[:4])
    # print(code)
    stock_dict = {}
    stock_dict['Name'] = 'maotai'
    return json.dumps(stock_dict)


@app.route("/getPrice", methods=["GET"])
def getPrice():
    stock_dict = {}
    stock_dict['Name'] = 'maotai'
    stock_dict['price'] = 14
    stock_dict['Previous Close'] = 13
    stock_dict['Open'] = 13.5
    stock_dict['Bid'] = 15
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
    app.run(debug=True, port=5006)
