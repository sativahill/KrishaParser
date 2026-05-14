from aiogram import Router
from aiogram.types import Message
from aiogram import F

from app.storage.repository import (
    ListingRepository
)

from app.services.scraper_service import (
    run_scraper
)

from app.bot.keyboards.listing_keyboards import (
    listing_keyboard
)

router = Router()


@router.message(
    F.text == "📦 Последние объявления"
)
async def listings_handler(message: Message):

    listings = (
        ListingRepository
        .get_all()
    )

    if not listings:

        await message.answer(
            "База пустая"
        )

        return

    response = "🏠 Последние объявления\n\n"

    for item in listings[-5:]:
        
        text = (
            f"🆔 {item.krisha_id}\n"
            f"💰 {item.price:,} ₸\n"
            f"🏠 {item.title}\n"
            f"📍 {item.address}"
        )

        await message.answer(
            text,
            reply_markup=listing_keyboard(
                item.krisha_id
            )
        )