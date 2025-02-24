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
import io
import base64
from bs4 import BeautifulSoup
import pandas as pd # rows列 columns行  (columns name, 即欄位名稱)

# 盤後資訊>個股日成交資訊---繪圖---
def DrawPlotSTOCK_DAY(data, stockNo):
    # 接收 DataFrame 作為參數
    # 將圖片轉換成 Base64 編碼的字串，方便在 Django 前端用 <img src="data:image/png;base64,..." />
    '''
    plt.figure(figsize=(x軸長度, y軸長度)) # 圖片大小
    plt.xlabel('日期', fontsize=16)  # x軸標題 標題字體大小 設定16
    plt.ylabel('股價', fontsize=16)  # y軸標題 標題字體大小
    plt.title(f'{stockNo}股價', fontsize=18) # 圖片標題(上方)
    '''    
    plt.figure(figsize=(10.0, 5.0))
    plt.xlabel('日期', fontsize=16)
    plt.ylabel('股價', fontsize=16)
    plt.title(f'{stockNo} 股價圖表', fontsize=18)
    '''
    plt.plot(data['日期'], data['收盤價'], color='red', markersize=16, marker='.') 
        plt.plot(x軸 根據'日期', y軸 根據'收盤價' 紅色實現 標記大小為16 標記符號為'.')
    plt.xticks(rotation=45) # x軸標題旋轉 45 度
    plt.rcParams["font.sans-serif"] = 'Microsoft JhengHei' # 字體轉換成Microsoft JhengHei
    plt.rcParams["axes.unicode_minus"] = False # 負號可正常顯示
    plt.show() # 顯示圖片
    '''
    plt.plot(data['日期'], data['收盤價'], color='red', markersize=16, marker='.')
    plt.xticks(rotation=45)
    plt.rcParams["font.sans-serif"] = 'Microsoft JhengHei'
    plt.rcParams["axes.unicode_minus"] = False # 允許負號顯示

    # 將圖片存入byteio，轉成Base64  
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight') # 解決圖片邊界問題bbox_inches='tight'
    plt.close() # 關閉圖表
    buffer.seek(0) # seek(0) start of stream (the default); offset should be zero or positive

    img_64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_64

# 盤後資訊>個股日成交資訊 stock_D_M
def stock_D_M(stock_code):
    date = datetime.now().strftime("%Y%m%d")  # 取得當前年月日
    
    stockNo = stock_code
    print('取得當前年月日:',date,' stockNo:',stockNo)
    url = f'https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date={date}&stockNo={stockNo}&response=html'
    resp=requests.get(url)

    # **讀取網頁數據，轉為 DataFrame**
    data = pd.read_html(resp.text)[0]
    data.columns = data.columns.droplevel(0) # 知道有哪些index(column name欄位名稱)
    data = data[['日期', '收盤價']]  # 只保留所需欄位

    # 假設 `data['日期']` 是 DataFrame 裡的日期欄位
    data['日期'] = data['日期'].apply(convert_tw_date)
    data['日期'] = pd.to_datetime(data['日期'], format="%Y/%m/%d")  # 轉換日期格式
    data['收盤價'] = pd.to_numeric(data['收盤價'], errors='coerce')  # 轉換數字格式

    img_base64 = DrawPlotSTOCK_DAY(data,stockNo)
    return img_base64

# 上市公司基本資料 stockInfo.py
def stockInfo(stock_code):
    date = datetime.now()
    infomationURL = 'opendata/t187ap03_L' # 上市公司基本資料
    URL = BaseTWSE_URL+infomationURL
    datas = requests.get(URL).json()
    for data in datas:
        if data['公司代號']==stock_code:
            return {
            '公司簡稱' : data['公司簡稱'],
            '公司名稱' : data['公司名稱'],
            '公司代號' : data['公司代號'],
            '電子郵件信箱' : data['電子郵件信箱'],
            '網址' : data['網址'],
            '發言人' : data['發言人'],
            '產業別代碼' : data['產業別'],
            '住址' : data['住址'],
            '營利事業統一編號' : data['營利事業統一編號'],
            '董事長' : data['董事長'],
            '總經理' : data['總經理'],
            '代理發言人' : data['代理發言人'],
            '總機電話' : data['總機電話'],
            '傳真機號碼' : data['傳真機號碼'],
            '成立日期' : data['成立日期'],
            '上市日期' : data['上市日期'],
            '普通股每股面額' : data['普通股每股面額'],
            '實收資本額' : data['實收資本額'],
            '股票過戶機構' : data['股票過戶機構'],
            '簽證會計師事務所' : data['簽證會計師事務所'],
            '已發行普通股數或TDR原股發行股數' : data['已發行普通股數或TDR原股發行股數']
            }                  

# 轉換民國年(YYY/MM/DD)轉換為西元年(YYYY/MM/DD)
def convert_tw_date(tw_date_str):
    parts = tw_date_str.split('/')
    if len(parts) == 3:
        year = str(int(parts[0]) + 1911)  # 轉換民國年為西元年
        return f"{year}/{parts[1]}/{parts[2]}"
    return tw_date_str  # 如果格式不對，則原樣返回

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
        stock_info_data = stockInfo(stockCodes)
        stock_D_M_img = stock_D_M(stockCodes) # 獲取繪圖 Base64

        cached_data = {
            'stock_code': stock_code_data,
            'stockInfo': stock_info_data ,
            'stock_D_M_img': stock_D_M_img  # **存入 Base64 圖片**
            }
        cache.set(cache_key,json.dumps(cached_data))
        return render(request,'stockCodes.html', cached_data)
    return render(request,'stockCodes.html', {})