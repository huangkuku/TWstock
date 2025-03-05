from django.shortcuts import render
import twstock
import requests
from utils.redis_utils import get_redis_connection
from django.core.cache import cache
import json
from templates.static.outputURL import BaseTWSE_URL # views.py上層stockCode與static/outputURL.py上層templates屬同一層
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # 不使用 GUI 介面
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties
import io
import yfinance as yf
import base64
from bs4 import BeautifulSoup
import pandas as pd # rows列 columns行  (columns name, 即欄位名稱)
from .models import StockDay
# 取得k線圖 5MA 10MA 20MA 60MA kline.py
def stock_day(stock_code):
    # 設定中文字型
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 設定為支援中文的字型，例如微軟正黑體
    plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

    # 使用 yfinance 獲取股價資料
    stock = yf.Ticker(stock_code+".TW")
    data = stock.history(period="90d")  # 獲取過去90天的資料

    # 計算移動平均線
    data['5MA'] = data['Close'].rolling(window=5).mean()
    data['10MA'] = data['Close'].rolling(window=10).mean()
    data['20MA'] = data['Close'].rolling(window=20).mean()
    data['60MA'] = data['Close'].rolling(window=60).mean()
    
    # 裁剪回最近31天資料
    data = data.iloc[-31:]

    # 將日期轉換為數值格式
    date_nums = [mdates.date2num(date) for date in data.index] # list
    formatted_dates = [date.strftime('%Y-%m-%d') for date in data.index]


    # 繪製K線圖和5MA
    plt.figure(figsize=(10, 6))

    for i in range(len(data)):
        Stock_date = date_nums[i]
        Close_price = data['Close'].iloc[i]  # 收盤
        Open_price = data['Open'].iloc[i]  # 開盤
        High = data['High'].iloc[i]
        Low = data['Low'].iloc[i]

        color = 'green'
        if Close_price > Open_price:  # 收盤>開盤 陽線 漲
            color = 'red'

        plt.bar(Stock_date, abs(Close_price - Open_price), bottom=min(Close_price, Open_price), width=0.5, color=color)
        plt.bar(Stock_date, High - Low, bottom=Low, width=0.1, color=color)

    # 繪製MA
    plt.plot(date_nums, data['5MA'], color='orange', linestyle='-', label='5MA', zorder=3)
    plt.plot(date_nums, data['10MA'], color='pink', linestyle='-', label='10MA', zorder=3)
    plt.plot(date_nums, data['20MA'], color='blue', linestyle='--', label='20MA', zorder=3)
    plt.plot(date_nums, data['60MA'], color='black', linestyle='-.', label='60MA', zorder=3)

    # 設定 x 軸日期格式
    plt.xticks(date_nums, formatted_dates, rotation=90)
    plt.xlabel('日期', fontsize=10)
    plt.ylabel('股價', fontsize=10)
    plt.legend()  # 顯示圖例
    plt.tight_layout()
    # plt.show()
    
    # 將圖片存入byteio，轉成Base64  
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight') # 解決圖片邊界問題bbox_inches='tight'
    plt.close() # 關閉圖表
    buffer.seek(0) # seek(0) start of stream (the default); offset should be zero or positive

    img_64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_64

def stockCodes(request):    
    if request.method == 'POST':   # 如果請求/request 的方法(method)是 POST
        # do something in here
        stockCodes=request.POST.get('stockCodes', '').strip() # request.POST['stockCodes'] = request.POST.get('stockCodes') strip()空白刪除
        if not stockCodes:
            msg = '請輸入股票代碼'
            return render(request, 'stockCodes.html', {'msg':msg})
        r = get_redis_connection()
        cache_key = f'stock_{stockCodes}'

        # 使用 Django Cache API 操作 Redis
        cached_data = cache.get(cache_key)
        # 如果 redis有資料
        if cached_data:
            print("從 Redis 取得快取數據")
            catch_data = json.loads(cached_data)            
            return render(request,'stockCodes.html',catch_data)

        print("從 爬蟲 取得數據") 
        # 判斷是否為台灣上市櫃股票(輸入代號查詢) 
        def getStockCodes(stock_code):
            if stock_code in twstock.codes[stockCodes]:                
                return {
                    '公司名稱':twstock.codes[stockCodes].name,
                    '股票代號':twstock.codes[stockCodes].code,
                    '市場別': twstock.codes[stockCodes].market,
                    '產業別':twstock.codes[stockCodes].group
                }
            else:
                return f'{stock_code}非台灣上市櫃股票代號'    
        stock_code_data = getStockCodes(stockCodes)
        stock_after_day = stock_day(stockCodes)
        cached_data = {
            'stock_code': stock_code_data,
            'stock_after_day':stock_after_day
            }
        cache.set(cache_key,json.dumps(cached_data))
        return render(request,'stockCodes.html', cached_data)
    return render(request,'stockCodes.html', {})