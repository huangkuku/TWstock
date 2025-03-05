from django.db import models
import json
# Create your models here.

# 根據views.py的data，data為從今天算起，過去90天的資料 資料型態是pandas.core.frame.DataFrame
# 及五日線data['5MA']、data['10MA']、data['20MA'] 及data['60MA']等'pandas.core.series.Series'數據
# 可以把資料轉成json格式，提取出來時再從json轉回原本的格式


class StockDay(models.Model):
    stock_code = models.CharField(max_length=10, primary_key=True) # 股票代碼 ex:2330
    stock_name = models.CharField(max_length=20)  # 股票代碼.TW ex: 2330.TW
    data_json = models.JSONField() # data為從今天算起，過去90天的資料 資料型態是pandas.core.frame.DataFrame
    ma5 = models.JSONField() # MA5是 data['5MA']，也就是5日線的資料 資料型態可能是pandas.core.series.Series，且裡面的數值為浮點數型態
    ma10 = models.JSONField() # MA10是 data['10MA']，也就是10日線的資料 資料型態可能是pandas.core.series.Series，且裡面的數值為浮點數型態
    ma20 = models.JSONField() # MA20是 data['20MA']，也就是20日線的資料 資料型態可能是pandas.core.series.Series，且裡面的數值為浮點數型態
    ma60 = models.JSONField() # MA60是 data['60MA']，也就是60日線的資料 資料型態可能是pandas.core.series.Series，且裡面的數值為浮點數型態
    date_nums = models.JSONField() # 日期格式 ex:2025-03-01 唯一個list，裡面的value是字串型態
    last_updated = models.DateTimeField() # 最後的更新日期

    def __str__(self):
        return f"股票代號: {self.stock_code}，最後更新時間: {self.last_updated}"
