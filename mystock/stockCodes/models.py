from django.db import models
import json
# Create your models here.

# 根據views.py的data，data為從今天算起，過去90天的資料 資料型態是pandas.core.frame.DataFrame
# 及五日線data['5MA']、data['10MA']、data['20MA'] 及data['60MA']等'pandas.core.series.Series'數據
# 可以把資料轉成json格式，提取出來時再從json轉回原本的格式


class StockDay(models.Model):
    stock_code = models.CharField(max_length=20, primary_key=True) # 股票代碼 ex:2330
    img_64 = models.TextField(blank=True, null=True)
    data_json = models.JSONField(blank=True, null=True) # data為從今天算起，過去90天的資料 資料型態是pandas.core.frame.DataFrame
    ma5 = models.JSONField(blank=True, null=True) # MA5是 data['5MA']，也就是5日線的資料 資料型態可能是pandas.core.series.Series，且裡面的數值為浮點數型態
    ma10 = models.JSONField(blank=True, null=True) # MA10是 data['10MA']，也就是10日線的資料 資料型態可能是pandas.core.series.Series，且裡面的數值為浮點數型態
    ma20 = models.JSONField(blank=True, null=True) # MA20是 data['20MA']，也就是20日線的資料 資料型態可能是pandas.core.series.Series，且裡面的數值為浮點數型態
    ma60 = models.JSONField(blank=True, null=True) # MA60是 data['60MA']，也就是60日線的資料 資料型態可能是pandas.core.series.Series，且裡面的數值為浮點數型態
    date_nums = models.JSONField(blank=True, null=True) # 日期格式 ex:2025-03-01 唯一個list，裡面的value是字串型態
    last_updated = models.DateTimeField(auto_now_add=True) # 最後的更新日期

    def __str__(self):
        return f"股票代號: {self.stock_code}，最後更新時間: {self.last_updated}"
