import logging

from aiogram.types import FSInputFile, ReplyKeyboardMarkup
from pydantic import BaseModel

from app.config import config
from app.keyboards.user import post_session_kb

logger = logging.getLogger(__name__)


class ScheduleMessage(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    text: str
    media_path: str | None
    # Seconds to wait AFTER this message before the next one is sent.
    delay_next_in_seconds: int
    keyboard: None | ReplyKeyboardMarkup


DEAL_80_MESSAGES = [
    ScheduleMessage(
        text=(
            "✅ Trade 1 Closed Successfully\n\n"
            "<b>Pair:</b> BTC/USDT\n"
            "<b>Direction:</b> SHORT\n"
            "<b>Start Amount:</b> £80.00\n"
            "<b>Close Amount:</b> £200.81\n"
            "<b>Profit:</b> +£120.81"
        ),
        media_path="assets/deals80/deal1.jpg",
        delay_next_in_seconds=32 * 60,
        keyboard=None,
    ),
    ScheduleMessage(
        text=(
            "✅ Trade 2 Closed Successfully\n\n"
            "<b>Pair:</b> SOL/USDT\n"
            "<b>Direction:</b> LONG\n"
            "<b>Start Amount:</b> £200.81\n"
            "<b>Close Amount:</b> £479.45\n"
            "<b>Profit:</b> +£278.64"
        ),
        media_path="assets/deals80/deal2.jpg",
        delay_next_in_seconds=26 * 60,
        keyboard=None,
    ),
    ScheduleMessage(
        text=(
            "✅ Trade 3 Closed Successfully\n\n"
            "<b>Pair:</b> ETH/USDT\n"
            "<b>Direction:</b> LONG\n"
            "<b>Start Amount:</b> £479.45\n"
            "<b>Close Amount:</b> £1,109.93\n"
            "<b>Profit:</b> +£630.48"
        ),
        media_path="assets/deals80/deal3.jpg",
        delay_next_in_seconds=45 * 60,
        keyboard=None,
    ),
    ScheduleMessage(
        text=(
            "✅ Trade 4 Closed Successfully\n\n"
            "<b>Pair:</b> LTC/USDT\n"
            "<b>Direction:</b> SHORT\n"
            "<b>Start Amount:</b> £1,109.93\n"
            "<b>Close Amount:</b> £2,488.80\n"
            "<b>Profit:</b> +£1,378.87"
        ),
        media_path="assets/deals80/deal4.jpg",
        delay_next_in_seconds=0,
        keyboard=post_session_kb(),
    ),
]

DEAL_150_MESSAGES = [
    ScheduleMessage(
        text=(
            "✅ Trade 1 Closed Successfully\n\n"
            "<b>Pair:</b> BTC/USDT\n"
            "<b>Direction:</b> SHORT\n"
            "<b>Start Amount:</b> £150.00\n"
            "<b>Close Amount:</b> £398.76\n"
            "<b>Profit:</b> +£248.76"
        ),
        media_path="assets/deals150/deal1.jpg",
        delay_next_in_seconds=65 * 60,
        keyboard=None,
    ),
    ScheduleMessage(
        text=(
            "✅ Trade 2 Closed Successfully\n\n"
            "<b>Pair:</b> SOL/USDT\n"
            "<b>Direction:</b> LONG\n"
            "<b>Start Amount:</b> £398.76\n"
            "<b>Close Amount:</b> £993.99\n"
            "<b>Profit:</b> +£595.23"
        ),
        media_path="assets/deals150/deal2.jpg",
        delay_next_in_seconds=75 * 60,
        keyboard=None,
    ),
    ScheduleMessage(
        text=(
            "✅ Trade 3 Closed Successfully\n\n"
            "<b>Pair:</b> ETH/USDT\n"
            "<b>Direction:</b> LONG\n"
            "<b>Start Amount:</b> £993.99\n"
            "<b>Close Amount:</b> £2,297.91\n"
            "<b>Profit:</b> +£1,303.92"
        ),
        media_path="assets/deals150/deal3.jpg",
        delay_next_in_seconds=61 * 60,
        keyboard=None,
    ),
    ScheduleMessage(
        text=(
            "✅ Trade 4 Closed Successfully\n\n"
            "<b>Pair:</b> LTC/USDT\n"
            "<b>Direction:</b> SHORT\n"
            "<b>Start Amount:</b> £2,297.91\n"
            "<b>Close Amount:</b> £4,987.76\n"
            "<b>Profit:</b> +£2,689.85"
        ),
        media_path="assets/deals150/deal4.jpg",
        delay_next_in_seconds=0,
        keyboard=post_session_kb(),
    ),
]

DEAL_1000_MESSAGES = [
    ScheduleMessage(
        text=(
            "✅ Trade 1 Closed Successfully\n\n"
            "<b>Pair:</b> BTC/USDT\n"
            "<b>Direction:</b> SHORT\n"
            "<b>Start Amount:</b> £1,000.00\n"
            "<b>Close Amount:</b> £2,184.30\n"
            "<b>Profit:</b> +£1,184.30"
        ),
        media_path="assets/deals1000/deal1.jpg",
        delay_next_in_seconds=65 * 60,
        keyboard=None,
    ),
    ScheduleMessage(
        text=(
            "✅ Trade 2 Closed Successfully\n\n"
            "<b>Pair:</b> SOL/USDT\n"
            "<b>Direction:</b> LONG\n"
            "<b>Start Amount:</b> £2,184.30\n"
            "<b>Close Amount:</b> £4,471.70\n"
            "<b>Profit:</b> +£2,287.40"
        ),
        media_path="assets/deals1000/deal2.jpg",
        delay_next_in_seconds=75 * 60,
        keyboard=None,
    ),
    ScheduleMessage(
        text=(
            "✅ Trade 3 Closed Successfully\n\n"
            "<b>Pair:</b> ETH/USDT\n"
            "<b>Direction:</b> LONG\n"
            "<b>Start Amount:</b> £4,471.70\n"
            "<b>Close Amount:</b> £8,656.32\n"
            "<b>Profit:</b> +£4,184.62"
        ),
        media_path="assets/deals1000/deal3.jpg",
        delay_next_in_seconds=61 * 60,
        keyboard=None,
    ),
    ScheduleMessage(
        text=(
            "✅ Trade 4 Closed Successfully\n\n"
            "<b>Pair:</b> LTC/USDT\n"
            "<b>Direction:</b> SHORT\n"
            "<b>Start Amount:</b> £8,656.32\n"
            "<b>Close Amount:</b> £15,678.42\n"
            "<b>Profit:</b> +£7,022.10"
        ),
        media_path="assets/deals1000/deal4.jpg",
        delay_next_in_seconds=0,
        keyboard=post_session_kb(),
    ),
]

# Plan amount -> ordered list of trade messages.
DEAL_MESSAGES: dict[int, list[ScheduleMessage]] = {
    80: DEAL_80_MESSAGES,
    150: DEAL_150_MESSAGES,
    1000: DEAL_1000_MESSAGES,
}

# Delay (seconds) from the moment the session starts until the first trade closes.
DEAL_START_DELAYS: dict[int, int] = {
    80: 25 * 60,
    150: 45 * 60,
    1000: 45 * 60,
}


async def send_deals(ctx, chat_id: int, plan: int, index: int = 0) -> None:
    """Send one trade message and schedule the next one after its delay.

    Runs as an arq task: each invocation sends `messages[index]` (with its
    image) and, if there is a following trade, re-enqueues itself deferred by
    the current message's `delay_next_in_seconds`.
    """
    messages = DEAL_MESSAGES.get(plan)
    if not messages or index >= len(messages):
        logger.info("STOPED SENDING DEALS")
        return

    message = messages[index]
    bot = ctx["bot"]

    if message.media_path:
        await bot.send_photo(
            chat_id,
            FSInputFile(message.media_path),
            caption=message.text,
            reply_markup=message.keyboard,
        )
    else:
        await bot.send_message(chat_id, message.text, reply_markup=message.keyboard)

    next_index = index + 1
    if next_index < len(messages):
        await ctx["redis"].enqueue_job(
            "send_deals",
            chat_id,
            plan,
            next_index,
            _defer_by=message.delay_next_in_seconds,
        )
