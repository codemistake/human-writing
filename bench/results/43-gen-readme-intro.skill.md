# ratelimit-redis

Ограничивает частоту запросов алгоритмом token bucket, храня состояние в Redis — лимит общий для всех инстансов приложения. Поддерживает asyncio.

## Установка

```
pip install ratelimit-redis
```

## Пример

```python
limiter = RedisRateLimiter(redis, key="api:user:42", rate=10, per=60)
if await limiter.allow():
    ...
```

Redis Cluster пока не поддерживается (в планах).

Лицензия — MIT.
