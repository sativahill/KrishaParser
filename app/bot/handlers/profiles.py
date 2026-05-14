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

from app.core.parsers import (
    normalize_rooms,
    normalize_range,
    normalize_price
)

router = Router()


PROPERTY_TYPES = {
    "квартира": "kvartiry",
    "дом": "doma-dachi",
}


# =====================================
# HELPERS
# =====================================

def format_range(
    min_value,
    max_value,
    suffix=""
):

    if not min_value and not max_value:
        return "не указано"

    if min_value and not max_value:
        return f"от {min_value}{suffix}"

    if min_value == max_value:
        return f"{min_value}{suffix}"

    return (
        f"{min_value}-{max_value}"
        f"{suffix}"
    )


def format_property_type(
    property_type: str
):

    mapping = {
        "kvartiry": "Квартира",
        "doma-dachi": "Дом",
    }

    return mapping.get(
        property_type,
        property_type
    )


# =====================================
# PROFILE
# =====================================

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

            property_type="kvartiry",

            city_slug="almaty",

            rooms="2,3",

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

        f"🏠 Тип: "
        f"{format_property_type(profile.property_type)}\n"

        f"📍 Город: "
        f"{profile.city_slug}\n"

        f"🛏 Комнаты: "
        f"{profile.rooms or 'не указаны'}\n"

        f"💰 Цена до: "
        f"{profile.price_to:,} ₸\n"

        f"📐 Площадь: "
        f"{format_range(profile.min_area, profile.max_area, ' м²')}\n"

        f"🏢 Этаж: "
        f"{format_range(profile.min_floor, profile.max_floor)}"
    )

    await message.answer(
        text,
        reply_markup=profile_keyboard()
    )


# =====================================
# SET TYPE
# =====================================

@router.message(
    ProfileStates.waiting_type
)
async def set_type(
    message: Message,
    state: FSMContext
):

    value = (
        message.text
        .strip()
        .lower()
    )

    property_type = PROPERTY_TYPES.get(
        value
    )

    if not property_type:

        await message.answer(
            "❌ Неверный тип\n\n"
            "Доступно:\n"
            "• квартира\n"
            "• дом"
        )

        return

    profiles = (
        SearchProfileRepository.get_all()
    )

    profile = profiles[0]

    profile.property_type = property_type

    # auto reset floor for houses
    if property_type == "doma-dachi":

        if (
            profile.min_floor
            and profile.min_floor > 3
        ):
            profile.min_floor = 3

        if (
            profile.max_floor
            and profile.max_floor > 3
        ):
            profile.max_floor = 3

    SearchProfileRepository.update_profile(
        profile
    )

    await state.clear()

    await message.answer(
        f"✅ Тип обновлен\n\n"
        f"🏠 {value}"
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
            "❌ Город не распознан\n\n"
            "Примеры:\n"
            "Алматы\n"
            "Астана\n"
            "Шымкент"
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
        f"✅ Город обновлен\n\n"
        f"📍 {profile.city_slug}"
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

    # houses usually don't need rooms filter
    if profile.property_type == "doma-dachi":

        await message.answer(
            "❌ Для домов фильтр комнат отключен"
        )

        return

    result = normalize_rooms(
        message.text
    )

    if not result:

        await message.answer(
            "❌ Неверный формат\n\n"
            "Примеры:\n"
            "2\n"
            "2,3\n"
            "2-4"
        )

        return

    profile.rooms = result["rooms"]

    SearchProfileRepository.update_profile(
        profile
    )

    await state.clear()

    await message.answer(
        f"✅ Комнаты обновлены\n\n"
        f"🛏 {profile.rooms}"
    )


# =====================================
# SET AREA
# =====================================

@router.message(
    ProfileStates.waiting_area
)
async def set_area(
    message: Message,
    state: FSMContext
):

    profiles = (
        SearchProfileRepository.get_all()
    )

    profile = profiles[0]

    max_area = 1000

    if profile.property_type == "doma-dachi":
        max_area = 3000

    result = normalize_range(
        message.text,
        min_limit=10,
        max_limit=max_area
    )

    if not result:

        await message.answer(
            "❌ Неверная площадь\n\n"
            "Примеры:\n"
            "45\n"
            "40-80"
        )

        return

    profile.min_area = result["min"]
    profile.max_area = result["max"]

    SearchProfileRepository.update_profile(
        profile
    )

    await state.clear()

    await message.answer(
        "✅ Площадь обновлена\n\n"

        f"📐 "
        f"{format_range(profile.min_area, profile.max_area, ' м²')}"
    )


# =====================================
# SET FLOOR
# =====================================

@router.message(
    ProfileStates.waiting_floor
)
async def set_floor(
    message: Message,
    state: FSMContext
):

    profiles = (
        SearchProfileRepository.get_all()
    )

    profile = profiles[0]

    max_floor = 50

    if profile.property_type == "doma-dachi":
        max_floor = 3

    result = normalize_range(
        message.text,
        min_limit=1,
        max_limit=max_floor
    )

    if not result:

        if profile.property_type == "doma-dachi":

            await message.answer(
                "❌ Для домов максимум 3 этажа\n\n"
                "Примеры:\n"
                "1\n"
                "1-2"
            )

        else:

            await message.answer(
                "❌ Неверный формат\n\n"
                "Примеры:\n"
                "3\n"
                "2-5"
            )

        return

    profile.min_floor = result["min"]
    profile.max_floor = result["max"]

    SearchProfileRepository.update_profile(
        profile
    )

    await state.clear()

    await message.answer(
        "✅ Этаж обновлен\n\n"

        f"🏢 "
        f"{format_range(profile.min_floor, profile.max_floor)}"
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

    price = normalize_price(
        message.text
    )

    if not price:

        await message.answer(
            "❌ Неверная цена\n\n"
            "Пример:\n"
            "30000000"
        )

        return

    profiles = (
        SearchProfileRepository.get_all()
    )

    profile = profiles[0]

    # anti impossible filters
    if (
        profile.property_type == "kvartiry"
        and price < 5_000_000
    ):

        await message.answer(
            "❌ Слишком маленькая цена для квартир"
        )

        return

    if (
        profile.property_type == "doma-dachi"
        and price < 10_000_000
    ):

        await message.answer(
            "❌ Слишком маленькая цена для домов"
        )

        return

    profile.price_to = price

    SearchProfileRepository.update_profile(
        profile
    )

    await state.clear()

    await message.answer(
        f"✅ Цена обновлена\n\n"
        f"💰 {profile.price_to:,} ₸"
    )