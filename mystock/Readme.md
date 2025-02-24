# TWstock

仿照 Yahoo 股市財報和健檢的應用程式

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
TWstock 是一個模仿 Yahoo 股市財報和健檢的應用程式，旨在提供用戶一個方便的工具來查看股票資訊和財務報告。

## 功能
- 顯示股票即時資訊(修改中)
- 財務報告檢視(修改中)
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
- Celery: 異步任務佇列
- Channels: 用於處理 WebSocket 和其他協定
- Matplotlib: 繪圖庫
- Pandas: 資料處理和分析
- Selenium: 自動化測試工具
- BeautifulSoup4: HTML 和 XML 解析器

## 如何使用
1. 啟動 Django 伺服器：
    ```bash
    python manage.py runserver
    ```
2. 開啟瀏覽器，訪問 `http://127.0.0.1:8000` 查看應用程式。

## 貢獻
歡迎任何形式的貢獻！請閱讀 [CONTRIBUTING.md](CONTRIBUTING.md) 了解更多資訊。

## 授權
此專案採用 MIT 授權，詳情請參閱 [LICENSE](LICENSE) 文件。