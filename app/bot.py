import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy

from app.config import config
from app.sql.db import create_pool
from app.middlewares.db_middleware import DataBaseMiddelware
from app.utils.redis import redis_factory

from app.handlers.basic import router as basic_router
from app.handlers.menu import router as menu_router
from app.handlers.admin.basic import router as admin_basic_router
from app.handlers.admin.generate_key import router as generate_key_router

logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("STARTING BOT")
    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    redis = redis_factory()
    session_factory = create_pool(config.db_dsn)

    await bot.delete_webhook(drop_pending_updates=True)
    dp = Dispatcher(
        fst_strategy=FSMStrategy.GLOBAL_USER, storage=RedisStorage(redis=redis)
    )
    dp["redis"] = redis
    dp.update.outer_middleware(DataBaseMiddelware(session_factory=session_factory))
    # Admin routers first: the catch-all code handler in basic_router must not
    # swallow admin commands/buttons, so basic_router is registered last.
    dp.include_router(admin_basic_router)
    dp.include_router(generate_key_router)
    dp.include_router(menu_router)
    dp.include_router(basic_router)

    # Expose the arq client to handlers so they can enqueue scheduler jobs.
    await dp.start_polling(bot)
