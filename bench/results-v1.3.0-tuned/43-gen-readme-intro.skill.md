# ratelimit-redis

Библиотека ограничивает частоту запросов по алгоритму token bucket и хранит состояние в Redis — значит, лимит общий для всех инстансов приложения, а не персональный для каждого процесса. Поддерживает asyncio.

Установка:

```
pip install ratelimit-redis
```

Минимальный пример:

```python
limiter = RedisRateLimiter(redis, key="api:user:42", rate=10, per=60)
if await limiter.allow():
    ...
```

Redis Cluster пока не поддерживается, это в планах. Лицензия — MIT.
