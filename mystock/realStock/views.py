from django.shortcuts import render
import redis
import json
from django.http import JsonResponse

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_real_stock(request):
    stock_code = request.GET.get('stock_code', '')  # 從 AJAX 請求取得股票代碼
    cache_key = f'stock_{stock_code}'
    stock_data = r.get(cache_key)

    if stock_data:
        return JsonResponse(json.loads(stock_data))
    else:
        return JsonResponse({'error': '沒有即時數據'}, status=404)
