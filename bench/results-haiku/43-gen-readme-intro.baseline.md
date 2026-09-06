# ratelimit-redis

Ограничение частоты запросов с помощью алгоритма token bucket, хранящего состояние в Redis. Работает с несколькими инстансами приложения — лимит общий для всех.

Поддерживает asyncio.

## Установка

```bash
pip install ratelimit-redis
```

## Быстрый старт

```python
from ratelimit_redis import RedisRateLimiter

limiter = RedisRateLimiter(redis, key="api:user:42", rate=10, per=60)

if await limiter.allow():
    # Обработать запрос
    pass
else:
    # Лимит исчерпан
    pass
```

Лицензия: MIT.

**Примечание:** Redis Cluster пока не поддерживается.