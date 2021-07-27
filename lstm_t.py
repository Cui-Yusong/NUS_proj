import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import tushare as ts
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

class LSTM_Predict:
    stock_code = ''
    tsData = pd.DataFrame()

    def __init__(self, stock_code):
        self.stock_code = stock_code
    def date_setting(self, start_date, end_date):
        self.tsData = ts.get_k_data(code=self.stock_code, start=start_date, end=end_date)
        self.tsData = self.tsData.sort_index(ascending=True).reset_index()
        print(self.tsData)
        return len(self.tsData)
    def makePrediction(self, node):
        # 创建数据框
        new_data = pd.DataFrame(index=range(0, len(self.tsData)), columns=['Date', 'Close'])
        self.tsData.index = pd.to_datetime(self.tsData.date)
        #new_data = new_data.sort_values(by='date')
        #new_data = self.tsData['close']
        for i in range(0, len(self.tsData)):
            new_data['Date'][i] = self.tsData.index[i]
            new_data['Close'][i] = self.tsData["close"][i]
        # 设置索引
        new_data.index = new_data.Date
        new_data.drop('Date', axis=1, inplace=True)
        #print(new_data)

        # 创建训练集和验证集
        dataset = new_data.values
        train = dataset[0:node, :]
        valid = dataset[node:, :]

        # 归一化
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset)
        # 将数据集转换为x_train和y_train
        x_train, y_train = [], []
        for i in range(60, len(train)):
            x_train.append(scaled_data[i - 60:i, 0])
            y_train.append(scaled_data[i, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # 创建和拟合LSTM网络
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(LSTM(units=50))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(x_train, y_train, epochs=5, batch_size=2, verbose=2)

        # 使用过去值来预测
        inputs = new_data[len(new_data) - len(valid) - 60:].values
        inputs = inputs.reshape(-1, 1)
        inputs = scaler.transform(inputs)
        X_test = []
        for i in range(60, inputs.shape[0]):
            X_test.append(inputs[i - 60:i, 0])
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        closing_price = model.predict(X_test)
        closing_price = scaler.inverse_transform(closing_price)

        # 作图
        train = new_data[:node]
        valid = new_data[node:]
        valid['Predictions'] = closing_price
        plt.plot(train['Close'],label='train')
        plt.plot(valid['Close'], label='actual',color='g')
        plt.plot(valid['Predictions'], label='predict',color='r')
        plt.legend()
        plt.xlabel('date')
        plt.ylabel('close price')
        plt.show()

stock_code = input('Please input the stock code: ')
start_date = input('Please input the start date with the format of "xx-xx-xx": ')
end_date = input('Please input the end date with the format of "xx-xx-xx": ')
    
mypred = LSTM_Predict(stock_code)
lenth = mypred.date_setting(start_date=start_date, end_date=end_date)
mypred.makePrediction(int(lenth*0.8))
