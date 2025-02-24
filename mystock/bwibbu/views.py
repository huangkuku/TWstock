from django.shortcuts import render
from templates.static.outputURL import BaseTWSE_URL
from utils.redis_utils import get_redis_connection
from django.core.cache import cache
import requests
import json
# 透過本益比、股利淨值比、現金殖利率等三個指標，評估目前股價合理程度 BWIBBU_ALL.py

BWIBBU_ALL = 'exchangeReport/BWIBBU_ALL' # 上市個股日本益比、殖利率及股價淨值比（依代碼查詢）
URL = BaseTWSE_URL+BWIBBU_ALL
def getDataJSON(URL):
    data = requests.get(URL).json()    
    return data

def getStockDetails(URL, **keyword):
    stock_code=keyword['stock_code']    
    results = getDataJSON(URL)
    for result in results:
        if result['Code']==stock_code:   
            return {
            '公司代碼':result['Code'], 
            '公司名稱':result['Name'], 
            '本益比':result['PEratio'], 
            '殖利率(%)':result['DividendYield'], 
            '股價淨值比':result['PBratio']
        }      
    return "your keyword is empty"

def bwibbu(request):
    if request.method=='POST':
        stockCodes=request.POST.get('stockCodes', '').strip()
        if not stockCodes:
            msg = '請輸入股票代碼'
            return render(request, 'bwibbu.html',{'msg':msg})
        r = get_redis_connection()
        cache_key = f'stock_{stockCodes}'
        # 使用 Django Cache API 操作 Redis
        cached_data = cache.get(cache_key)

        # 如果 redis有資料
        if cached_data:
            print("從 Redis 取得快取數據")
            catch_data = json.loads(cached_data)            
            return render(request,'bwibbu.html',{'cached_data':cached_data})
        print("從 爬蟲 取得數據") 

        cached_data = getStockDetails(URL, stock_code=stockCodes)
        cache.set(cache_key,json.dumps(cached_data))
        return render(request, 'bwibbu.html',{'cached_data':cached_data})
    
    return render(request, 'bwibbu.html',{'cached_data':''})
# 指標 1：本益比＝股價 ÷ 每股盈餘 ▶▶▶ 越低越好 (合理的本益比，平均大約是15 倍，本益比超過20 倍，那就太貴囉！)
# 指標 2：殖利率＝現金股利 ÷ 股價 ▶▶▶ 越高越好(台股過去五年的平均殖利率約為3.74%。 若某股票的殖利率達到5%，可以視為表現
# 相當不錯的投資標的。 但若殖利率低於銀行定存利率（約2%），該股票可能不適合長期持有。)
# 指標 3：股價淨值比＝股價 ÷ 每股淨值 ▶▶▶ 介於 1～2 倍（1 倍以下＝低估，2 倍以上＝高估）
