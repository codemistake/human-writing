Ограничение частоты запросов на алгоритме token bucket, состояние хранится в Redis - значит лимит общий для всех инстансов приложения, а не для каждого процесса отдельно. Работает на asyncio.

```
pip install ratelimit-redis
```

```python
limiter = RedisRateLimiter(redis, key="api:user:42", rate=10, per=60)
if await limiter.allow():
    ...
```

Лицензия MIT. Redis Cluster пока не поддерживается, в планах.
