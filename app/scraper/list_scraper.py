import re

from bs4 import BeautifulSoup

from app.storage.models import Listing

from app.core.logger import app_logger


async def parse_listing_cards(html: str):

    soup = BeautifulSoup(
        html,
        "lxml"
    )

    cards = soup.select(
        ".a-card"
    )

    listings = []

    for card in cards:

        try:

            link_element = card.select_one(
                "a.a-card__title"
            )

            if not link_element:
                continue

            href = link_element.get("href")

            if not href:
                continue

            full_url = (
                f"https://krisha.kz{href}"
            )

            id_match = re.search(
                r'/show/(\d+)',
                href
            )

            if not id_match:
                continue

            krisha_id = int(
                id_match.group(1)
            )

            title = (
                link_element
                .get_text(strip=True)
            )

            price_element = card.select_one(
                ".a-card__price"
            )

            price = 0

            if price_element:

                price_text = (
                    price_element
                    .get_text(strip=True)
                    .replace("\xa0", "")
                    .replace("〒", "")
                    .replace(" ", "")
                )

                digits = "".join(
                    filter(str.isdigit, price_text)
                )

                if digits:
                    price = int(digits)

            address_element = card.select_one(
                ".a-card__subtitle"
            )

            address = None

            if address_element:
                address = (
                    address_element
                    .get_text(strip=True)
                )

            listing = Listing(
                krisha_id=krisha_id,

                title=title,

                price=price,

                address=address,

                url=full_url
            )

            listings.append(listing)

        except Exception as e:

            app_logger.error(
                f"Card parse error: {e}"
            )

    return listings