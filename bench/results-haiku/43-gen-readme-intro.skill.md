ratelimit-redis ограничивает частоту запросов с помощью алгоритма token bucket. Состояние хранится в Redis, так что лимит общий для нескольких инстансов приложения.

Поддерживает asyncio.

```bash
pip install ratelimit-redis
```

Минимальный пример:

```python
limiter = RedisRateLimiter(redis, key="api:user:42", rate=10, per=60)
if await limiter.allow():
    # обработать запрос
```

MIT License.

Примечание: Redis Cluster не поддерживается, планируется добавить.
