from rapidfuzz import fuzz


CITIES = {
    "almaty": [
        "алматы",
        "алмата",
        "almaty",
    ],

    "astana": [
        "астана",
        "astana",
        "нур султан",
        "нурсултан",
    ],

    "shymkent": [
        "шымкент",
        "shymkent",
    ],

    "karaganda": [
        "караганда",
        "karagandy",
        "karaganda",
    ],

    "aktau": [
        "актау",
        "aktau",
    ],

    "atyrau": [
        "атырау",
        "atyrau",
    ],

    "aktobe": [
        "актобе",
        "aktobe",
    ],

    "kostanay": [
        "костанай",
        "kostanai",
        "kostanay",
    ],

    "kyzylorda": [
        "кызылорда",
        "kyzylorda",
    ],

    "oskemen": [
        "усть каменогорск",
        "усть-каменогорск",
        "оскемен",
        "ust kamenogorsk",
        "oskemen",
    ],

    "pavlodar": [
        "павлодар",
        "pavlodar",
    ],

    "semey": [
        "семей",
        "semei",
        "semey",
    ],

    "taraz": [
        "тараз",
        "taraz",
    ],

    "turkestan": [
        "туркестан",
        "turkestan",
    ],

    "oral": [
        "уральск",
        "oral",
        "uralsk",
    ],

    "petropavlovsk": [
        "петропавловск",
        "petropavlovsk",
    ],

    "kokshetau": [
        "кокшетау",
        "kokshetau",
    ],
}


def normalize_city(
    user_input: str
):

    if not user_input:
        return None

    text = (
        user_input
        .strip()
        .lower()
    )

    # exact
    for slug, aliases in CITIES.items():

        if text in aliases:
            return slug

    # fuzzy
    best_score = 0
    best_slug = None

    for slug, aliases in CITIES.items():

        for alias in aliases:

            score = fuzz.ratio(
                text,
                alias
            )

            if score > best_score:
                best_score = score
                best_slug = slug

    if best_score >= 80:
        return best_slug

    return None