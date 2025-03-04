import twstock 
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#設定爬蟲股票代號
sid = '2365'
#設定爬蟲時間
start = datetime.datetime.now() - datetime.timedelta(days=180)
end = datetime.date.today()
#用fetch_from抓取資料，並放入dataframe裡
data=twstock.Stock(sid)
data.fetch_from(2025,2)
#指定日期放入dataframe裡
stock_tw = pd.DataFrame(data.fetch_from(2025,2))
stock_tw.tail(10)
# print(stock_tw.tail(10))
#線型圖，收盤價、5日均線、20日均線、60日均線
stock_tw['close'].plot(figsize=(16, 8))
stock_tw['close'].rolling(window=5).mean().plot(figsize=(16, 8), label='5_Day_Mean')
stock_tw['close'].rolling(window=20).mean().plot(figsize=(16, 8), label='20_Day_Mean')
stock_tw['close'].rolling(window=60).mean().plot(figsize=(16, 8), label='60_Day_Mean')

#顯示側標
plt.legend(loc='upper right', shadow=True, fontsize='x-large')

#顯示標題
plt.title(sid+'_twstock')
plt.show()