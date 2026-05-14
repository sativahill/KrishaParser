from playwright.async_api import (
    TimeoutError
)

from app.core.logger import (
    app_logger
)

from app.messenger.templates import (
    get_random_template
)


async def send_message(
    page,
    listing
):

    try:

        await page.goto(
            listing.url,
            wait_until="domcontentloaded",
            timeout=20000
        )

        await page.wait_for_timeout(5000)

        # =====================================
        # CHAT BUTTONS
        # =====================================

        chat_button_texts = [
            "Написать",
            "Написать сообщение",
            "Связаться",
            "Чат"
        ]

        # =====================================
        # CALLBACK BUTTONS
        # =====================================

        callback_button_texts = [
            "Заказать обратный звонок",
            "Обратный звонок"
        ]

        clicked = False

        # =====================================
        # TRY CHAT BUTTON
        # =====================================

        for text in chat_button_texts:

            try:

                button = page.get_by_text(
                    text,
                    exact=False
                )

                if await button.count() > 0:

                    await button.first.click()

                    clicked = True

                    break

            except:
                pass

        # =====================================
        # CALLBACK ONLY
        # =====================================

        if not clicked:

            for text in callback_button_texts:

                try:

                    button = page.get_by_text(
                        text,
                        exact=False
                    )

                    if await button.count() > 0:

                        app_logger.warning(
                            f"Callback only: "
                            f"{listing.krisha_id}"
                        )

                        return "CALLBACK_ONLY"

                except:
                    pass

        # =====================================
        # NO CHAT
        # =====================================

        if not clicked:

            app_logger.warning(
                f"Chat button not found: "
                f"{listing.krisha_id}"
            )

            return "NO_CHAT"

        await page.wait_for_timeout(4000)

        # =====================================
        # MESSAGE TEMPLATE
        # =====================================

        message = get_random_template()

        textarea_selectors = [
            "textarea",
            '[contenteditable="true"]',
            "input[type='text']"
        ]

        typed = False

        for selector in textarea_selectors:

            try:

                textarea = page.locator(
                    selector
                )

                if await textarea.count() > 0:

                    await textarea.first.fill(
                        message
                    )

                    await page.wait_for_timeout(
                        1500
                    )

                    await textarea.first.press(
                        "Enter"
                    )

                    typed = True

                    break

            except:
                pass

        if not typed:

            app_logger.warning(
                f"Message input not found: "
                f"{listing.krisha_id}"
            )

            return "INPUT_NOT_FOUND"

        await page.wait_for_timeout(3000)

        app_logger.success(
            f"Message sent: "
            f"{listing.krisha_id}"
        )

        return "SUCCESS"

    except TimeoutError:

        app_logger.error(
            "Message timeout"
        )

        return "TIMEOUT"

    except Exception as e:

        app_logger.error(
            f"Message send error: {e}"
        )

        return "ERROR"
    
async def request_callback(
    page,
    listing
):

    try:

        await page.goto(
            listing.url,
            wait_until="domcontentloaded",
            timeout=20000
        )

        await page.wait_for_timeout(5000)

        callback_button_texts = [
            "Заказать обратный звонок",
            "Обратный звонок"
        ]

        clicked = False

        for text in callback_button_texts:

            try:

                button = page.get_by_text(
                    text,
                    exact=False
                )

                if await button.count() > 0:

                    await button.first.click()

                    clicked = True

                    break

            except:
                pass

        if not clicked:

            return "NOT_FOUND"

        await page.wait_for_timeout(3000)

        app_logger.success(
            f"Callback requested: "
            f"{listing.krisha_id}"
        )

        return "SUCCESS"

    except Exception as e:

        app_logger.error(
            f"Callback request error: {e}"
        )

        return "ERROR"