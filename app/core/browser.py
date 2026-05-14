from playwright.async_api import async_playwright
from playwright_stealth import Stealth

from app.core.config import config
from app.core.anti_detect import get_random_user_agent

playwright_instance = None
browser_context = None


async def start_browser():
    global playwright_instance
    global browser_context

    playwright_instance = await async_playwright().start()

    browser_context = await playwright_instance.chromium.launch_persistent_context(
        user_data_dir=config.PROFILE_PATH,

        headless=config.HEADLESS,

        viewport={
            "width": 1366,
            "height": 768
        },

        user_agent=get_random_user_agent(),

        locale="ru-RU",

        timezone_id="Asia/Almaty",

        args=[
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
        ]
    )

    return browser_context


async def get_page():
    global browser_context

    page = await browser_context.new_page()

    stealth = Stealth()

    await stealth.apply_stealth_async(page)

    return page


async def stop_browser():
    global browser_context
    global playwright_instance

    if browser_context:
        await browser_context.close()

    if playwright_instance:
        await playwright_instance.stop()