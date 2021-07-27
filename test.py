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

t = 1620921600000.00000
t = t/1000
an = time.localtime(t)
print(an)