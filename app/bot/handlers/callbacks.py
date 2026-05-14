from aiogram import Router
from aiogram.types import CallbackQuery

from aiogram.fsm.context import (
    FSMContext
)

from app.bot.states import (
    ProfileStates
)

from app.storage.repository import (
    ListingRepository,
    SearchProfileRepository
)

from app.core.browser import (
    start_browser,
    stop_browser,
    get_page
)

from app.scraper.phone_scraper import (
    parse_phone
)

from app.messenger.sender import (
    send_message,
    request_callback
)

from app.services.scraper_service import (
    run_scraper
)

from app.core.state import (
    active_users
)

from app.auth.auth_service import (
    is_logged_in
)

from app.bot.keyboards.listing_keyboard import (
    listing_keyboard
)

router = Router()


@router.callback_query()
async def callback_handler(
    callback: CallbackQuery,
    state: FSMContext
):

    data = callback.data

    await callback.answer()

    if not data:
        return

    user_id = callback.from_user.id

    # =====================================
    # ACTION LOCK
    # =====================================

    if user_id in active_users:

        await callback.answer(
            "⏳ Подождите",
            show_alert=False
        )

        return

    active_users.add(user_id)

    try:

        # =====================================
        # EDIT TYPE
        # =====================================

        if data == "edit_type":

            await state.set_state(
                ProfileStates.waiting_type
            )

            await callback.message.answer(
                "🏠 Тип недвижимости\n\n"
                "Доступно:\n"
                "• квартира\n"
                "• дом"
            )

            return

        # =====================================
        # EDIT CITY
        # =====================================

        elif data == "edit_city":

            await state.set_state(
                ProfileStates.waiting_city
            )

            await callback.message.answer(
                "📍 Введите город\n\n"
                "Например:\n"
                "Алматы\n"
                "Астана"
            )

            return

        # =====================================
        # EDIT ROOMS
        # =====================================

        elif data == "edit_rooms":

            await state.set_state(
                ProfileStates.waiting_rooms
            )

            await callback.message.answer(
                "🛏 Введите комнаты\n\n"
                "Примеры:\n"
                "234\n"
                "2,3\n"
                "2-4"
            )

            return

        # =====================================
        # EDIT PRICE
        # =====================================

        elif data == "edit_price":

            await state.set_state(
                ProfileStates.waiting_price
            )

            await callback.message.answer(
                "💰 Введите максимальную цену\n\n"
                "Пример:\n"
                "30000000"
            )

            return

        # =====================================
        # EDIT AREA
        # =====================================

        elif data == "edit_area":

            await state.set_state(
                ProfileStates.waiting_area
            )

            await callback.message.answer(
                "📐 Введите площадь\n\n"
                "Примеры:\n"
                "45\n"
                "40-80"
            )

            return

        # =====================================
        # EDIT FLOOR
        # =====================================

        elif data == "edit_floor":

            await state.set_state(
                ProfileStates.waiting_floor
            )

            await callback.message.answer(
                "🏢 Введите этаж\n\n"
                "Примеры:\n"
                "3\n"
                "2-5"
            )

            return

        # =====================================
        # RUN PROFILE
        # =====================================

        elif data == "run_profile":

            profiles = (
                SearchProfileRepository
                .get_all()
            )

            if not profiles:

                await callback.answer(
                    "❌ Профиль не найден",
                    show_alert=True
                )

                return

            profile = profiles[0]

            status_message = await callback.message.answer(
                "🔍 Ищу объявления..."
            )

            listings = await run_scraper(
                profile
            )

            await status_message.delete()

            if not listings:

                await callback.answer(
                    "❌ Объявления не найдены",
                    show_alert=True
                )

                return

            for item in listings:

                text = (
                    f"🏠 {item.title}\n"
                    f"💰 {item.price:,} ₸\n"
                    f"📍 {item.address}"
                )

                await callback.message.answer(
                    text,
                    reply_markup=listing_keyboard(
                        item.krisha_id
                    )
                )

        # =====================================
        # PHONE CALLBACK
        # =====================================

        elif data.startswith("phone:"):

            krisha_id = int(
                data.split(":")[1]
            )

            status_message = await callback.message.answer(
                "📞 Получаю номер..."
            )

            listings = (
                ListingRepository.get_all()
            )

            listing = None

            for item in listings:

                if item.krisha_id == krisha_id:
                    listing = item
                    break

            if not listing:

                await status_message.edit_text(
                    "❌ Объявление не найдено"
                )

                return

            if listing.phone:

                await status_message.edit_text(
                    f"📱 {listing.phone}"
                )

                return

            await start_browser()

            page = await get_page()

            await page.goto(
                "https://krisha.kz",
                wait_until="domcontentloaded"
            )

            logged_in = await is_logged_in(
                page
            )

            if not logged_in:

                await stop_browser()

                await status_message.edit_text(
                    "❌ Аккаунт Krisha разлогинен"
                )

                return

            updated_listing = await parse_phone(
                page,
                listing
            )

            if updated_listing.phone:

                updated_listing.status = (
                    "PHONE_PARSED"
                )

            ListingRepository.update_listing(
                updated_listing
            )

            await stop_browser()

            if updated_listing.phone:

                await status_message.edit_text(
                    f"📱 {updated_listing.phone}"
                )

            else:

                await status_message.edit_text(
                    "❌ Телефон не найден"
                )

        # =====================================
        # MESSAGE CALLBACK
        # =====================================

        elif data.startswith("message:"):

            krisha_id = int(
                data.split(":")[1]
            )

            status_message = await callback.message.answer(
                "💬 Отправляю сообщение..."
            )

            listings = (
                ListingRepository.get_all()
            )

            listing = None

            for item in listings:

                if item.krisha_id == krisha_id:
                    listing = item
                    break

            if not listing:

                await status_message.edit_text(
                    "❌ Объявление не найдено"
                )

                return

            if listing.status == "CONTACTED":

                await status_message.edit_text(
                    "✅ Сообщение уже отправлено"
                )

                return

            await start_browser()

            page = await get_page()

            await page.goto(
                "https://krisha.kz",
                wait_until="domcontentloaded"
            )

            logged_in = await is_logged_in(
                page
            )

            if not logged_in:

                await stop_browser()

                await status_message.edit_text(
                    "❌ Аккаунт Krisha разлогинен"
                )

                return

            result = await send_message(
                page,
                listing
            )

            await stop_browser()

            if result == "SUCCESS":

                listing.status = (
                    "CONTACTED"
                )

                ListingRepository.update_listing(
                    listing
                )

                await status_message.edit_text(
                    "✅ Сообщение отправлено"
                )

            elif result == "CALLBACK_ONLY":

                await status_message.edit_text(
                    "☎ Чат недоступен"
                )

                await callback.message.answer(
                    "📲 Можно запросить обратный звонок",
                    reply_markup=listing_keyboard(
                        listing.krisha_id,
                        callback_only=True
                    )
                )

            elif result == "NO_CHAT":

                await status_message.edit_text(
                    "❌ Чат недоступен"
                )

            else:

                await status_message.edit_text(
                    "❌ Не удалось отправить"
                )

        # =====================================
        # REQUEST CALLBACK
        # =====================================

        elif data.startswith(
            "request_callback:"
        ):

            krisha_id = int(
                data.split(":")[1]
            )

            listings = (
                ListingRepository.get_all()
            )

            listing = None

            for item in listings:

                if item.krisha_id == krisha_id:
                    listing = item
                    break

            if not listing:

                await callback.answer(
                    "❌ Объявление не найдено",
                    show_alert=True
                )

                return

            await callback.answer(
                "📲 Отправляю запрос..."
            )

            await start_browser()

            page = await get_page()

            result = await request_callback(
                page,
                listing
            )

            await stop_browser()

            if result == "SUCCESS":

                await callback.answer(
                    "✅ Запрос отправлен",
                    show_alert=True
                )

            else:

                await callback.answer(
                    "❌ Не удалось отправить",
                    show_alert=True
                )

    finally:

        active_users.discard(user_id)