from bs4 import BeautifulSoup

from app.core.logger import app_logger


async def parse_listing_details(page, listing):

    try:

        await page.goto(
            listing.url,
            wait_until="domcontentloaded"
        )

        await page.wait_for_timeout(3000)

        html = await page.content()

        soup = BeautifulSoup(
            html,
            "lxml"
        )

        description_element = soup.select_one(
            ".a-description__text"
        )

        if description_element:

            listing.description = (
                description_element
                .get_text(strip=True)
            )

        info_blocks = soup.select(
            ".offer__info-item"
        )

        for block in info_blocks:

            text = block.get_text(
                " ",
                strip=True
            )

            if "Этаж" in text:
                listing.floor = text

            if "Площадь" in text:
                listing.area = text

        app_logger.success(
            f"Parsed details: "
            f"{listing.krisha_id}"
        )

        return listing

    except Exception as e:

        app_logger.error(
            f"Detail parse error: {e}"
        )

        return listing