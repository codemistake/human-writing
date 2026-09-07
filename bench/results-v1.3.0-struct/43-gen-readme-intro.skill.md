# ratelimit-redis

Ограничивает частоту запросов по алгоритму token bucket, храня состояние в Redis — это позволяет держать общий лимит на несколько инстансов приложения. Поддерживает asyncio.

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
