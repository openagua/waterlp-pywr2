from loguru import logger

try:
    import os
    import redis

    local_redis = redis.Redis(host=os.environ.get('REDIS_HOST', 'localhost'), port=6379, db=0)
    local_redis.get('test')

except:
    logger.warning('Redis not available.')
    local_redis = None
