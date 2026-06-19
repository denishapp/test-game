import asyncio
import json
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("shahed-bot")

# --- configuration -----------------------------------------------------
# Set these as environment variables before running the bot, e.g.:
#   export BOT_TOKEN="123456:ABC-..."
#   export WEBAPP_URL="https://your-username.github.io/shahed-game/"
BOT_TOKEN = os.environ["BOT_TOKEN"]
WEBAPP_URL = os.environ["WEBAPP_URL"]

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


def play_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎮 Грати", web_app=WebAppInfo(url=WEBAPP_URL))]
        ]
    )


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Привіт! 🌃 Над містом з'явились ворожі шахеди — допоможи їх збити.\n\n"
        "Веди турель пальцем по екрану, вона стріляє автоматично. "
        "Лови ⚡ за збитий дрон — пришвидшує стрільбу. Не дай дронам прорватись!",
        reply_markup=play_keyboard(),
    )


@dp.message(F.web_app_data)
async def on_webapp_data(message: Message) -> None:
    """Triggered when the game sends a result via Telegram.WebApp.sendData()."""
    try:
        data = json.loads(message.web_app_data.data)
        score = int(data.get("score", 0))
        wave = int(data.get("wave", 1))
    except (ValueError, TypeError, AttributeError):
        await message.answer("Дякую за гру! 🎮")
        return

    name = message.from_user.first_name or "Гравець"
    await message.answer(
        f"🎯 <b>{name}</b> збив(ла) <b>{score}</b> дронів і дійшов(шла) до хвилі <b>{wave}</b>!",
        reply_markup=play_keyboard(),
    )


async def main() -> None:
    log.info("Starting bot, webapp url: %s", WEBAPP_URL)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
