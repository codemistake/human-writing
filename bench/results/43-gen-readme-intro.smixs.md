# ratelimit-redis

Ограничение частоты запросов по алгоритму token bucket. Состояние хранится в Redis, поэтому лимит общий для всех инстансов приложения, а не отдельный для каждого процесса.

Поддерживает asyncio.

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

Лицензия - MIT.
