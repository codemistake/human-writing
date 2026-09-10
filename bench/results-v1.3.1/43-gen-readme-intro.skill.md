# ratelimit-redis

Ограничивает частоту запросов по алгоритму token bucket, храня состояние в Redis — это значит, что лимит общий для всех инстансов приложения, а не для каждого процесса отдельно. Поддерживает asyncio.

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

Лицензия — MIT.
