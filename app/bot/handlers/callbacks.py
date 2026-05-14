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
    send_message
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

        await callback.message.answer(
            "⏳ Дождитесь завершения предыдущей операции"
        )

        return

    active_users.add(user_id)

    try:

        # =====================================
        # EDIT CITY
        # =====================================

        if data == "edit_city":

            await state.set_state(
                ProfileStates.waiting_city
            )

            await callback.message.answer(
                "📍 Введите новый город:"
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
                "🏠 Введите комнаты:\n"
                "Например: 2,3,4"
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
                "💰 Введите максимальную цену:"
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

                await callback.message.answer(
                    "❌ Профиль не найден"
                )

                return

            profile = profiles[0]

            status_message = await callback.message.answer(
                "🔍 Запускаю поиск..."
            )

            count = await run_scraper(
                profile
            )

            await status_message.edit_text(
                f"✅ Обработано объявлений: "
                f"{count}"
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
                    "❌ Аккаунт Krisha разлогинен\n"
                    "Перелогиньтесь через main.py"
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
                    "❌ Аккаунт Krisha разлогинен\n"
                    "Перелогиньтесь через main.py"
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
                    "☎ Доступен только обратный звонок"
                )

            elif result == "NO_CHAT":

                await status_message.edit_text(
                    "❌ Чат недоступен"
                )

            else:

                await status_message.edit_text(
                    "❌ Не удалось отправить"
                )

    finally:

        active_users.discard(user_id)