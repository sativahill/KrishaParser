import asyncio

from aiogram import Bot
from aiogram import Dispatcher

from app.bot.handlers.menu import (
    router
)

from app.bot.handlers.listings import (
    router as listings_router
)

from app.bot.handlers.callbacks import (
    router as callbacks_router
)


from app.storage.database import (
    create_db_and_tables
)

from app.bot.handlers.export import (
    router as export_router
)

from app.bot.handlers.profiles import (
    router as profiles_router
)

from app.core.config import config


async def main():

    create_db_and_tables()

    bot = Bot(
        token=config.BOT_TOKEN
    )

    dp = Dispatcher()

    dp.include_router(router)
    dp.include_router(listings_router)
    dp.include_router(callbacks_router)
    dp.include_router(export_router)
    dp.include_router(profiles_router)

    print("BOT STARTED")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())