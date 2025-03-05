# TWstock

台灣上市上櫃公司盤後股票資料的應用程式

## 目錄
- [TWstock](#twstock)
  - [目錄](#目錄)
  - [專案介紹](#專案介紹)
  - [功能](#功能)
  - [安裝](#安裝)
  - [使用技術](#使用技術)
  - [如何使用](#如何使用)
  - [貢獻](#貢獻)
  - [授權](#授權)

## 專案介紹
TWstock 是一個呈現台灣股票K線圖、5MA、10MA、20MA、60MA的應用程式，旨在提供用戶一個方便的工具來查看股票資訊分析買賣市場。

## 功能
- 股票技術分析圖表
- 自動化數據抓取

## 安裝
1. 克隆此專案到本地：
    ```bash
    git clone https://github.com/huangkuku/TWstock.git
    ```
2. 安裝依賴：
    ```bash
    pip install -r mystock/requirements.txt
    ```

## 使用技術
- Django: 後端框架
- Redis: 用於快取和訊息佇列
- PostgreSQL: 股票資料存取置資料庫
- Matplotlib: 繪圖庫
- Pandas: 資料處理和分析
- Selenium: 自動化測試工具
- BeautifulSoup4: HTML 和 XML 解析器

## 如何使用
1. 本地資料庫PostgreSQL
   1. 建立server: TWstock (可能需要密碼: 參照mystock/mystock/settings.py DATABASES = {...,'PASSWORD': '設定的密碼',...})
   2. 建立database: stocks
2. docker運行redis
   1. ``` docker pull redis```
   2. ``` docker run  --name redis -p 6379:6379 -d redis
3. migrate database
   1. ``` python manage.py makemigrations```
   2. ``` python manage.py migrate```
4. 啟動 Django 伺服器：
    ```bash
    python manage.py runserver
   ```
5. 開啟瀏覽器，訪問 `http://127.0.0.1:8000` 查看應用程式。

## 貢獻
歡迎任何形式的貢獻！請閱讀 [CONTRIBUTING.md](CONTRIBUTING.md) 了解更多資訊。

## 授權
此專案採用 MIT 授權，詳情請參閱 [LICENSE](LICENSE) 文件。