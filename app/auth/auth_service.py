from app.core.logger import (
    app_logger
)


async def is_logged_in(page) -> bool:

    try:

        current_url = page.url

        if "login" in current_url:
            return False

        auth_selectors = [
            'a[href*="/my"]',
            '.profile-menu',
            '.user-menu',
            '[data-testid="user-menu"]'
        ]

        for selector in auth_selectors:

            try:

                element = page.locator(
                    selector
                )

                if await element.count() > 0:
                    return True

            except:
                pass

        return False

    except Exception as e:

        app_logger.error(
            f"Auth check error: {e}"
        )

        return False