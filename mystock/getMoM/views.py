# 月營收年增率連續三個月大於0 getMoM.py
# 月營收年增率 計算公式＝(當月營收－去年同期) / 去年同期*100%。 
# (202412-202312)/202312*100%  (202411-202311)/202311*100%  (202410-202310)/202310*100%
from django.shortcuts import render
from django.core.cache import cache
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
from bs4 import BeautifulSoup
import re
import requests
import redis
from utils.redis_utils import get_redis_connection
import json
from datetime import datetime

URL = "https://mops.twse.com.tw/mops/web/t146sb05" # 公開資訊觀測站精華版

# 營收報表提取api
def get_financial_table(search_key):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(URL)
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "co_id"))
        )
        search_input.clear()
        search_input.send_keys(search_key + Keys.RETURN)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "company"))
        )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        company_div = soup.find('div', {'id': 'company'})
        
        tables = company_div.find_all('table')
        if len(tables) < 3:
            return pd.DataFrame()
        
        revenue_table = tables[2]

        current_year = datetime.now().year
        prev_year = current_year - 1
        taiwan_current_year = current_year - 1911
        taiwan_prev_year = prev_year - 1911
        
        data_dict = {}
        current_key = None
        for tr in revenue_table.find_all('tr'):
            if 'thbg' in tr.get('class', []):
                tds = tr.find_all('td')
                if len(tds) >= 1:
                    current_key = tds[0].text.strip()
            elif 'text_center' in tr.get('class', []):
                if current_key:
                    values = [td.text.strip() for td in tr.find_all('td')]
                    data_dict[current_key] = values
                    current_key = None
        
        formatted_data = []
        for key, values in data_dict.items():
            if key.startswith(f'{taiwan_current_year}年') or key.startswith(f'{taiwan_prev_year}年'):
                year = current_year if key.startswith(f"{taiwan_current_year}年") else prev_year
                month = key.split('年')[1].split('月')[0].zfill(2)
                date = f"{year}/{month}"
                monthly_revenue = int(values[0].replace(',', '')) * 1000
                yoy_growth = float(values[2].replace(',', '').replace('%', ''))
                formatted_data.append([date, monthly_revenue, yoy_growth])
        
        return pd.DataFrame(formatted_data, columns=['年度/月份', '當月營收(仟元)', '年增率'])
    
    except Exception as e:
        print(f"處理錯誤: {str(e)}")
        return pd.DataFrame()
    finally:
        driver.quit()

# catch data
def getMoMdata(stockCodes):
        search_key = stockCodes
        r = get_redis_connection()
        cache_key = search_key
        # 使用 Django Cache API 操作 Redis
        cached_data = cache.get(cache_key)

        if cached_data:
            print("從 Redis 取得快取數據")
            return json.loads(cached_data)

        print("從 爬蟲 取得數據")
        result_df = get_financial_table(search_key)
        if not result_df.empty:
            current1 = result_df.at[0, '年增率']
            current2 = result_df.at[1, '年增率']
            current3 = result_df.at[2, '年增率']

            if current1 > 0 and current2 > 0 and current3 > 0:
                result = f'{stockCodes} 月營收年增率連續三個月大於0'
            else:
                result = f'{stockCodes} 月營收年增率未連續三個月大於0'
            
            # 轉換為 JSON 格式，方便前端處理
            data_list = result_df.values.tolist()
            cache.set(cache_key,json.dumps({"data": data_list, "result": result}))
            return {'data': data_list, 'result': result}
        
        return {'data': [], 'result': "查無相關營收資訊"}
    
def getMoM(request):
    if request.method == 'POST':
        stockCodes = request.POST['stockCodes']
        datas = getMoMdata(stockCodes)
        print(datas)
        return render(request, 'getMoM.html', {'data': datas['data'], 'result': datas['result']})
    return render(request, 'getMoM.html', {'data': [], 'result': ''})


