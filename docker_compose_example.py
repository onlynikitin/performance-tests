from redis import Redis

cache = Redis(host="redis", port=6379)
cache.set("example", 10)
print(int(cache.get("example")) ** 2)
