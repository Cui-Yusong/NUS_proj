import tushare as ts
import pandas as pd
from datetime import datetime
pro = ts.pro_api()

today_date = datetime.now().strftime('%Y%m%d')
#df = pro.bak_basic(trade_date=today_date)
df = pro.bak_basic(trade_date='20210723')
df = df.drop(['list_date','area','holder_num','reserved','reserved_pershare','undp','trade_date','per_undp','total_assets','liquid_assets','fixed_assets'],axis=1)
df = df.loc[df['pb']<3]
df = df.loc[df['pe']<15]
df = df.loc[df['pb']>0]
df = df.loc[df['pe']>0]

csv_data = pd.read_csv('C:\\Users\\Lenovo\\Desktop\\proj\\roe_3years.csv', index_col=0, low_memory = False)
roe_df = pd.DataFrame(csv_data)

res = pd.merge(roe_df,df)
res = res[['code','name','roe','pe','pb','gpr','npr','industry']]
res = res.loc[res['gpr']>0]
res = res.loc[res['npr']>0]

def create_stock_pool():
    #存储编码
    #settlement为昨日收盘价
    #暂时将昨日收盘价前10位股票加入股票池
    stock_pool = {}
    for i in range(0, len(res)):
        t1,t2 = res.iloc[i]['code'],res.iloc[i]['name']
        stock_pool[t1]=t2
    return stock_pool

if __name__ == '__main__':
    #market = all_stock()
    #which_col = input('Please input the column name: ')
    #sortby = sort_by_col(market,'settlement').head(10)
    stock_pool = create_stock_pool()
    print(stock_pool)

