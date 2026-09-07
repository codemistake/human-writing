# ratelimit-redis

Ограничение частоты запросов (алгоритм token bucket) с хранением состояния в Redis — лимит общий для всех инстансов приложения. Поддерживает asyncio.

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

Лицензия MIT. Redis Cluster пока не поддерживается (в планах).
