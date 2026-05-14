from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[

        [
            KeyboardButton(
                text="⚙ Профиль поиска"
            )
        ],

        [
            KeyboardButton(
                text="📦 Последние объявления"
            )
        ],

        [
            KeyboardButton(
                text="📤 Экспорт Excel"
            )
        ]

    ],

    resize_keyboard=True
)