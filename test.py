import time
import pandas as pd
import numpy as np

# a = ['Name', 'Age', 'Gender']
# b = ['Ali', '19', 'China']
# data = pd.DataFrame(zip(a, b), columns=['project', 'attribute'])

# test = {"t1":1,"t2":2,"t3":3}
# data=pd.DataFrame(test,index=[1])
# print (type(data))
# dict_country = data.to_dict()
# print (dict_country)

# t = 1620921600000.00000
# t = t/1000
# an = time.localtime(t)
# print(an)
import random

data=[]
df=pd.DataFrame()
for i in range(500):
    temp=[]
    for j in range(25):
        temp.append(random.randint(2,10))
    data.append(temp)
df.loc[:,"test"] =data
df.loc[:,'eee'] = data

df['test2']=data
print(df)