from app.core.browser import (
    start_browser,
    stop_browser,
    get_page
)

from app.search.url_builder import (
    build_search_url
)

from app.scraper.list_scraper import (
    parse_listing_cards
)

from app.scraper.detail_scraper import (
    parse_listing_details
)

from app.storage.repository import (
    ListingRepository
)

from app.storage.database import (
    create_db_and_tables
)


async def run_scraper(profile):

    create_db_and_tables()

    await start_browser()

    page = await get_page()

    rooms = [
        int(room.strip())
        for room in profile.rooms.split(",")
    ]

    search_url = build_search_url(
        city_slug=profile.city_slug,
        rooms=rooms,
        price_to=profile.price_to,
        page=1
    )

    await page.goto(
        search_url,
        wait_until="domcontentloaded"
    )

    await page.wait_for_timeout(5000)

    html = await page.content()

    listings = await parse_listing_cards(
        html
    )

    listings = listings[:5]

    saved_listings = []

    for listing in listings:

        saved_listing = (
            ListingRepository
            .create_listing(listing)
        )

        detailed_listing = (
            await parse_listing_details(
                page,
                saved_listing
            )
        )

        ListingRepository.update_listing(
            detailed_listing
        )

        saved_listings.append(
            detailed_listing
        )

    await stop_browser()

    return saved_listings