import asyncio
import logging
from datetime import timedelta

import orjson
from arq import ArqRedis
from redis.asyncio import ConnectionPool, SSLConnection

from app.config import config
from app.services.scheduler.job_serializer import job_serializer

logger = logging.getLogger(__name__)


def redis_factory() -> ArqRedis:
    kwargs = {
        "host": config.redis.host,
        "port": config.redis.port,
        "db": config.redis.db,
        "username": config.redis.username,
        "password": config.redis.password,
    }

    if config.redis.ssl:
        kwargs["connection_class"] = SSLConnection
        kwargs["ssl_cert_reqs"] = config.redis.ssl_cert_reqs
        kwargs["ssl_check_hostname"] = False

    logger.info(f"Redis connection params: {kwargs}")

    pool = ConnectionPool(**kwargs)

    # Match the worker's (de)serialization and default queue so jobs enqueued
    # from the bot are picked up and decoded correctly.
    redis = ArqRedis(
        connection_pool=pool,
        job_serializer=job_serializer,
        job_deserializer=orjson.loads,
        default_queue_name="queue:ai-trading-bot-dred",
    )
    return redis


async def gcra_limit(redis: ArqRedis, key: str, limit: int, period: timedelta) -> bool:
    period_in_seconds = int(period.total_seconds())
    t = await redis.time()
    current_time = t[0]
    separation = round(period_in_seconds / limit)
    await redis.setnx(key, 0)
    value = await redis.get(key)
    tat = max(int(value), current_time)
    if tat - current_time <= period_in_seconds - separation:
        new_tat = max(tat, current_time) + separation
        await redis.set(key, new_tat)
        return True
    return False


async def wait_for_gcra_limit(
    redis: ArqRedis, key: str, limit: int = 30, period: timedelta = timedelta(seconds=1)
) -> None:
    while True:
        wait = await gcra_limit(redis, key, limit, period)
        if wait:
            break
        await asyncio.sleep(0.5)
