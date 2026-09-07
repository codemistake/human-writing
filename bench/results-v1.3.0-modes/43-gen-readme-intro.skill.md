ratelimit-redis ограничивает частоту запросов по алгоритму token bucket, храня состояние в Redis, — поэтому лимит общий для всех инстансов приложения, а не для одного процесса. Поддерживает asyncio.

```bash
pip install ratelimit-redis
```

```python
limiter = RedisRateLimiter(redis, key="api:user:42", rate=10, per=60)
if await limiter.allow():
    ...
```

Redis Cluster пока не поддерживается, это в планах.

Лицензия — MIT.
