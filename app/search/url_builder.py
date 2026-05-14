from urllib.parse import urlencode


def build_search_url(
    city_slug: str,
    rooms: list[int],
    price_to: int,
    page: int = 1
):

    base_url = (
        f"https://krisha.kz/prodazha/"
        f"kvartiry/{city_slug}/"
    )

    params = [
        ("das[who]", "1")
    ]

    for room in rooms:

        params.append(
            ("das[live.rooms][]", str(room))
        )

    params.append(
        ("das[price][to]", str(price_to))
    )

    params.append(
        ("page", str(page))
    )

    query = urlencode(params)

    return f"{base_url}?{query}"