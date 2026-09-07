# ratelimit-redis

Ограничение частоты запросов по алгоритму token bucket, состояние хранится в Redis.

Смысл в общем состоянии: если приложение работает в нескольких инстансах, лимит один на всех, а не свой у каждого процесса. Поддерживается asyncio.

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

10 запросов за 60 секунд на ключ `api:user:42`. `allow()` возвращает False, когда лимит исчерпан.

## Ограничения

Redis Cluster пока не поддерживается, поддержка планируется.

## Лицензия

MIT
