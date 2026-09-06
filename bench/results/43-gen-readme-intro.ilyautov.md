# ratelimit-redis

Ограничение частоты запросов по алгоритму token bucket, состояние хранится в Redis. Значит лимит общий для всех инстансов приложения, а не для каждого по отдельности. Поддерживается asyncio.

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

Redis Cluster пока не поддерживается, в планах.

Лицензия: MIT.
