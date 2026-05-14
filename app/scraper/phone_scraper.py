import re

from app.core.logger import app_logger


async def parse_phone(page, listing):

    try:

        await page.goto(
            listing.url,
            wait_until="domcontentloaded",
            timeout=20000
        )

        await page.wait_for_timeout(4000)

        phone_button_texts = [
            "Показать телефон",
            "Показать телефоны"
        ]

        clicked = False

        for text in phone_button_texts:

            try:

                button = page.get_by_text(
                    text,
                    exact=False
                )

                if await button.count() > 0:

                    await button.first.click()

                    clicked = True

                    break

            except Exception:
                continue

        if not clicked:

            app_logger.warning(
                f"Phone button not found: "
                f"{listing.krisha_id}"
            )

            return listing

        await page.wait_for_timeout(3000)

        body_text = await page.locator(
            "body"
        ).inner_text()

        phones = re.findall(
            r'(\+7[\d\s\-\(\)]{9,})',
            body_text
        )

        if phones:

            cleaned_phone = (
                phones[0]
                .replace(" ", "")
                .replace("-", "")
            )

            listing.phone = cleaned_phone

            app_logger.success(
                f"Phone parsed: "
                f"{listing.phone}"
            )

        return listing

    except Exception as e:

        app_logger.error(
            f"Phone parse error: {e}"
        )

        return listing