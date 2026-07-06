from asyncio import CancelledError

import orjson
import pytz
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from arq import ArqRedis, Worker

from app.config import config
from app.sql.db import create_pool

from .job_serializer import job_serializer
from .tasks.message import send_deals


def interval_to_values(interval: int, max_value: int) -> set[int]:
    return set(range(0, max_value, interval))


async def startup(ctx) -> None:
    ctx["bot"] = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode="HTML", link_preview_is_disabled=True),
    )
    ctx["session_factory"] = create_pool(config.db_dsn)
    ctx["fsm_storage"] = RedisStorage(redis=ctx["redis"])


async def shutdown(ctx) -> None:
    pass


async def run_worker(redis: ArqRedis) -> None:
    worker = Worker(
        queue_name="queue:ai-trading-bot-dred",
        redis_pool=redis,
        functions=[send_deals],
        cron_jobs=[],
        job_serializer=job_serializer,
        job_completion_wait=120,
        job_deserializer=orjson.loads,
        max_jobs=2,
        on_startup=startup,
        on_shutdown=shutdown,
        job_timeout=216000,
        timezone=pytz.timezone("Europe/Kiev"),  # type: ignore
    )

    try:
        await worker.async_run()
    except CancelledError:
        raise

    finally:
        await worker.close()
