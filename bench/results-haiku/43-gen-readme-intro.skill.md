## ratelimit-redis

Ограничение частоты запросов (rate limiting) с состоянием в Redis. Используйте, когда нужно, чтобы лимит был общим для нескольких инстансов приложения. Алгоритм — token bucket.

Поддерживает asyncio.

### Установка

```bash
pip install ratelimit-redis
```

### Использование

```python
from ratelimit_redis import RedisRateLimiter

limiter = RedisRateLimiter(redis, key="api:user:42", rate=10, per=60)

if await limiter.allow():
    # обработать запрос
else:
    # вернуть 429
```

Лимит `rate=10, per=60` означает максимум 10 запросов в 60 секунд.

### Ограничения

Redis Cluster не поддерживается. Это в планах.

Лицензия: MIT