from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def listing_keyboard(
    krisha_id: int,
    callback_only: bool = False
):

    keyboard_rows = [
        [
            InlineKeyboardButton(
                text="📞 Телефон",
                callback_data=f"phone:{krisha_id}"
            )
        ]
    ]

    # =====================================
    # CHAT OR CALLBACK
    # =====================================

    if callback_only:

        keyboard_rows.append(
            [
                InlineKeyboardButton(
                    text="📲 Запросить звонок",
                    callback_data=f"request_callback:{krisha_id}"
                )
            ]
        )

    else:

        keyboard_rows.append(
            [
                InlineKeyboardButton(
                    text="💬 Написать",
                    callback_data=f"message:{krisha_id}"
                )
            ]
        )

    # =====================================
    # OPEN
    # =====================================

    keyboard_rows.append(
        [
            InlineKeyboardButton(
                text="🌐 Открыть",
                url=f"https://krisha.kz/a/show/{krisha_id}"
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard_rows
    )