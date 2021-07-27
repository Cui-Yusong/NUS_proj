import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts
from sklearn import preprocessing


ts.set_token('b11ee55fd1f2c78f551b05ad1ec41b336a8d8b8c75f3a2f2ce5d0ea4')   #需要在 tushare 官网申请一个账号，然后得到 token 后才能通过数据接口获取数据
pro = ts.pro_api()

df = pro.daily(ts_code='000001.SZ', start_date='2015-01-01', end_date='2020-02-25')

df.head()



df = df.iloc[::-1]
df.reset_index(inplace=True)

training_set = df.loc[:, ['close']]

training_set = training_set.values

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)

X_train = []
y_train = []
for i in range(60, len(training_set_scaled)):
    X_train.append(training_set_scaled[i-60:i])
    y_train.append(training_set_scaled[i, training_set_scaled.shape[1] - 1])
X_train, y_train = np.array(X_train), np.array(y_train)


from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

regressor = Sequential()
 
regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], X_train.shape[2])))
regressor.add(Dropout(0.2))
 
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))
 
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

regressor.add(Dense(units = 1))

regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

regressor.fit(X_train, y_train, epochs = 10, batch_size = 32)


import tushare as ts

ts.set_token('b11ee55fd1f2c78f551b05ad1ec41b336a8d8b8c75f3a2f2ce5d0ea4')
pro = ts.pro_api()

df_test = pro.daily(ts_code='000001.SZ', start_date='2021-01-01', end_date='2021-05-27')
df_test = pd.DataFrame(df_test, columns = ['ts_code','trade_date','close','open','high','low'])


df_test = df_test.iloc[::-1]
df_test.reset_index(inplace=True)

dataset_test = df_test.loc[:, ['close']]
dataset_total = pd.concat((df_test[['close']],df[['close']]))

inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
inputs = inputs.reshape(-1, dataset_test.shape[1])

inputs = sc.transform(inputs)

predicted_stock_price = []

#准备测试数据，就是把要测试的数据和以前训练的数据结合起来组装出要测试的 X，因为是要利用过去 60 个交易日的数据，只靠一个交易日的收盘价是不够的
X_test = []

for i in range(60, 60 + len(dataset_test)):
    X_test.append(inputs[i-60:i])
X_test = np.array(X_test)

# print(X_test)
 
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], dataset_test.shape[1]))

predicted_stock_price = regressor.predict(X_test)

#再把规则化数据转回成正常的价格数据，现在就可以得出预测的下个交易日收盘价格
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

print(predicted_stock_price)


# In[ ]:




