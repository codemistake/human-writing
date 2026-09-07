# ratelimit-redis

Ограничение частоты запросов по алгоритму token bucket, с состоянием в Redis. Лимит общий для всех инстансов приложения, а не для каждого процесса отдельно.

Работает поверх asyncio.

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

Redis Cluster пока не поддерживается, это в планах.

Лицензия - MIT.
