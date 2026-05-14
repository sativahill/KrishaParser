from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.bot.keyboards.main_menu import (
    main_menu
)

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):

    await message.answer(
        "🏠 Krisha Parser Bot",
        reply_markup=main_menu
    )