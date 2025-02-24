import redis
from django.conf import settings

# settings.py 讀取redis設定
redis_config = settings.REDIS_CONFIG

# redis 連線
r = redis.Redis(**redis_config)

# 連線的function
def get_redis_connection():
    # 獲取redis連線
    return r