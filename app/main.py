import asyncio

from app.core.browser import (
    start_browser,
    stop_browser,
    get_page
)

from app.core.logger import (
    app_logger
)


async def main():

    app_logger.info(
        "Starting browser..."
    )

    await start_browser()

    page = await get_page()

    await page.goto(
        "https://krisha.kz",
        wait_until="domcontentloaded"
    )

    app_logger.success(
        "Browser opened"
    )

    print("\n")
    print("=" * 50)
    print("LOGIN TO KRISHA ACCOUNT")
    print("PRESS ENTER AFTER LOGIN")
    print("=" * 50)
    print("\n")

    input()

    app_logger.success(
        "Session saved"
    )

    await stop_browser()

    app_logger.info(
        "Browser closed"
    )


if __name__ == "__main__":
    asyncio.run(main())