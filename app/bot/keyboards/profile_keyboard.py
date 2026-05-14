from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def profile_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="✏ Город",
                    callback_data="edit_city"
                )
            ],

            [
                InlineKeyboardButton(
                    text="✏ Комнаты",
                    callback_data="edit_rooms"
                )
            ],

            [
                InlineKeyboardButton(
                    text="✏ Цена",
                    callback_data="edit_price"
                )
            ],

            [
                InlineKeyboardButton(
                    text="▶ Запустить поиск",
                    callback_data="run_profile"
                )
            ]
        ]
    )