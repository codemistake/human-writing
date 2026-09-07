# ratelimit-redis

Ограничение частоты запросов по алгоритму token bucket. Состояние хранится в Redis, поэтому лимит общий для всех инстансов приложения. Есть поддержка asyncio.

## Установка

```bash
pip install ratelimit-redis
```

## Пример

```python
limiter = RedisRateLimiter(redis, key="api:user:42", rate=10, per=60)
if await limiter.allow():
    ...
```

## Ограничения

Redis Cluster не поддерживается, поддержка запланирована.

## Лицензия

MIT
