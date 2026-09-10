ratelimit-redis — ограничение частоты запросов (token bucket) с состоянием в Redis. Работает на нескольких инстансах приложения одновременно, поддерживает asyncio.

```bash
pip install ratelimit-redis
```

```python
limiter = RedisRateLimiter(redis, key="api:user:42", rate=10, per=60)
if await limiter.allow():
    # обработать запрос
```

Лицензия MIT. Поддерживает Redis 4+, но не поддерживает Redis Cluster (планируется).
