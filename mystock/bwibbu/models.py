from django.db import models

# Create your models here.
class BWIBBU(models.Model):
    stock_code = models.CharField(max_length=10, primary_key=True)  # 股票代碼
    name = models.CharField(max_length=50, null=True)  # 股票名稱
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # 本益比
    dividend_yield = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)# 殖利率(%)
    pb_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)# 股價淨值比(%)
    last_updated = models.DateTimeField(auto_now=True)             # 最後更新時間
    
    def __str__(self):
        return f"股票代碼:{self.stock_code},股票名稱:{self.Name}" 
    class Meta:
        db_table = 'bwibbu_stock_data'   # 自訂資料表名稱