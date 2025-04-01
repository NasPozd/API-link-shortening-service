import redis

redis_client = redis.Redis(host='redis', port=6379, db=0)

def set_cache(key: str, value: str):
    redis_client.set(key, value)

def get_cache(key: str) -> str:
    return redis_client.get(key)
