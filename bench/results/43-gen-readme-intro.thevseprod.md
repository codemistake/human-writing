# ratelimit-redis

Ограничение частоты запросов по алгоритму token bucket с состоянием в Redis - лимит общий для всех инстансов приложения, а не для каждого процесса отдельно.

Поддерживает asyncio.

```
pip install ratelimit-redis
```

```python
limiter = RedisRateLimiter(redis, key="api:user:42", rate=10, per=60)
if await limiter.allow():
    ...
```

Redis Cluster пока не поддерживается, в планах.

Лицензия MIT.