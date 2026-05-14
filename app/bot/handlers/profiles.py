from aiogram import Router
from aiogram.types import Message
from aiogram import F

from aiogram.fsm.context import FSMContext

from app.storage.models import (
    SearchProfile
)

from app.storage.repository import (
    SearchProfileRepository
)

from app.bot.keyboards.profile_keyboard import (
    profile_keyboard
)

from app.bot.states import (
    ProfileStates
)

from app.core.cities import (
    normalize_city
)

router = Router()


@router.message(
    F.text == "⚙ Профиль поиска"
)
async def profile_handler(
    message: Message
):

    profiles = (
        SearchProfileRepository.get_all()
    )

    if not profiles:

        default_profile = SearchProfile(
            name="ACTIVE",

            city_slug="karaganda",

            rooms="2,3,4",

            price_to=50000000
        )

        SearchProfileRepository.create_profile(
            default_profile
        )

        profiles = (
            SearchProfileRepository.get_all()
        )

    profile = profiles[0]

    text = (
        f"⚙ Текущий профиль\n\n"

        f"📍 Город: "
        f"{profile.city_slug}\n"

        f"🏠 Комнаты: "
        f"{profile.rooms}\n"

        f"💰 Цена до: "
        f"{profile.price_to:,} ₸"
    )

    await message.answer(
        text,
        reply_markup=profile_keyboard()
    )


# =====================================
# SET CITY
# =====================================

@router.message(
    ProfileStates.waiting_city
)
async def set_city(
    message: Message,
    state: FSMContext
):

    city_slug = normalize_city(
        message.text
    )

    if not city_slug:

        await message.answer(
            "❌ Город не распознан"
        )

        return

    profiles = (
        SearchProfileRepository.get_all()
    )

    profile = profiles[0]

    profile.city_slug = city_slug

    SearchProfileRepository.update_profile(
        profile
    )

    await state.clear()

    await message.answer(
        f"✅ Город обновлен:\n"
        f"{profile.city_slug}"
    )


# =====================================
# SET ROOMS
# =====================================

@router.message(
    ProfileStates.waiting_rooms
)
async def set_rooms(
    message: Message,
    state: FSMContext
):

    profiles = (
        SearchProfileRepository.get_all()
    )

    profile = profiles[0]

    profile.rooms = (
        message.text.strip()
    )

    SearchProfileRepository.update_profile(
        profile
    )

    await state.clear()

    await message.answer(
        f"✅ Комнаты обновлены:\n"
        f"{profile.rooms}"
    )


# =====================================
# SET PRICE
# =====================================

@router.message(
    ProfileStates.waiting_price
)
async def set_price(
    message: Message,
    state: FSMContext
):

    profiles = (
        SearchProfileRepository.get_all()
    )

    profile = profiles[0]

    try:

        profile.price_to = int(
            message.text.strip()
        )

    except:

        await message.answer(
            "❌ Введите число"
        )

        return

    SearchProfileRepository.update_profile(
        profile
    )

    await state.clear()

    await message.answer(
        f"✅ Цена обновлена:\n"
        f"{profile.price_to:,} ₸"
    )