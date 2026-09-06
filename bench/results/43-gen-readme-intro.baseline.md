# ratelimit-redis

Ограничение частоты запросов по алгоритму token bucket с хранением состояния в Redis — лимит общий для всех инстансов приложения. Поддерживает asyncio.

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

## Ограничения

Redis Cluster пока не поддерживается (в планах).

## Лицензия

MIT
