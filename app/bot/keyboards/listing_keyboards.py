from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def listing_keyboard(krisha_id: int):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📞 Телефон",
                    callback_data=f"phone:{krisha_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬 Написать",
                    callback_data=f"message:{krisha_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌐 Открыть",
                    url=f"https://krisha.kz/a/show/{krisha_id}"
                )
            ]
        ]
    )

    return keyboard