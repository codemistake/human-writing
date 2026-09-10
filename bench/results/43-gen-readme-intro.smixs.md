# ratelimit-redis

Ограничение частоты запросов по алгоритму token bucket с хранением состояния в Redis. Пригодится, если лимит должен быть общим для нескольких инстансов приложения, а не для каждого по отдельности.

Поддерживает asyncio.

```bash
pip install ratelimit-redis
```

```python
limiter = RedisRateLimiter(redis, key="api:user:42", rate=10, per=60)

if await limiter.allow():
    ...
```

Redis Cluster пока не поддерживается, но это в планах.

Лицензия - MIT.
