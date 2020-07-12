import aioredis


async def get(khash):
    redis = await aioredis.create_redis_pool("redis://localhost")
    result = await redis.hgetall(khash, encoding="utf-8")
    redis.close()
    await redis.wait_closed()
    return result


async def put(khash, val):
    redis = await aioredis.create_redis_pool("redis://localhost")
    await redis.hmset_dict(khash, val)
    redis.close()
    await redis.wait_closed()


async def delete(khash):
    redis = await aioredis.create_redis_pool("redis://localhost")
    await redis.delete(khash)
    redis.close()
    await redis.wait_closed()
