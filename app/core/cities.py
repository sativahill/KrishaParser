from rapidfuzz import process


VALID_CITIES = {

    "almaty": [
        "алматы",
        "алмати",
        "алмата",
        "almaty"
    ],

    "astana": [
        "астана",
        "астан",
        "astana",
        "нур-султан"
    ],

    "karaganda": [
        "караганда",
        "карагнда",
        "karaganda"
    ],

    "shymkent": [
        "шымкент",
        "шимкент",
        "shymkent"
    ],

    "aktau": [
        "актау",
        "aktau"
    ],

    "atyrau": [
        "атырау",
        "atyrau"
    ]
}


def normalize_city(
    user_input: str
):

    user_input = (
        user_input
        .strip()
        .lower()
    )

    all_variants = {}

    for city_slug, variants in VALID_CITIES.items():

        for variant in variants:

            all_variants[variant] = city_slug

    match = process.extractOne(
        user_input,
        all_variants.keys()
    )

    if not match:
        return None

    matched_text = match[0]

    score = match[1]

    # =====================================
    # MIN CONFIDENCE
    # =====================================

    if score < 70:
        return None

    return all_variants[
        matched_text
    ]