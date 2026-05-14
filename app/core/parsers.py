import re


MAX_PRICE = 500_000_000

MAX_FLOOR = 50

MAX_AREA = 1000

MIN_AREA = 10


VALID_ROOMS = {
    "1",
    "2",
    "3",
    "4",
    "5"
}


# =====================================
# ROOMS
# =====================================

def normalize_rooms(
    user_input: str
):

    original_input = (
        user_input
        .strip()
        .lower()
    )

    if not original_input:
        return None

    # =====================================
    # SINGLE
    # =====================================

    if original_input in VALID_ROOMS:

        return {
            "rooms": original_input,
            "normalized": False
        }

    # =====================================
    # 234
    # =====================================

    if (
    original_input.isdigit()
    and len(original_input) <= 5
    ):

     rooms = []

    for char in original_input:

        if char in VALID_ROOMS:
            rooms.append(char)

    rooms = sorted(
        list(set(rooms))
    )

    if not rooms:
        return None

    return {
        "rooms": ",".join(rooms),
        "normalized": True
    }

    # =====================================
    # 2,3,4
    # =====================================

    perfect_match = re.fullmatch(
        r"[1-5](,[1-5])*",
        original_input
    )

    if perfect_match:

        rooms = sorted(
            list(
                set(
                    original_input.split(",")
                )
            )
        )

        return {
            "rooms": ",".join(rooms),
            "normalized": False
        }

    # =====================================
    # 2-4
    # =====================================

    range_match = re.fullmatch(
        r"([1-5])\s*-\s*([1-5])",
        original_input
    )

    if range_match:

        start = int(
            range_match.group(1)
        )

        end = int(
            range_match.group(2)
        )

        if start > end:
            start, end = end, start

        rooms = [
            str(i)
            for i in range(start, end + 1)
        ]

        return {
            "rooms": ",".join(rooms),
            "normalized": True
        }

    return None


# =====================================
# RANGE
# =====================================

def normalize_range(
    user_input: str,
    *,
    min_limit: int,
    max_limit: int
):

    original_input = (
        user_input
        .strip()
        .lower()
    )

    if not original_input:
        return None

    # =====================================
    # SINGLE NUMBER
    # =====================================

    if original_input.isdigit():

        value = int(original_input)

        if value <= 0:
            return None

        if value < min_limit:
            return None

        if value > max_limit:
            return None

        return {
            "min": value,
            "max": None,
            "normalized": False
        }

    # =====================================
    # RANGE
    # =====================================

    range_match = re.fullmatch(
        r"(\d+)\s*-\s*(\d+)",
        original_input
    )

    if range_match:

        start = int(
            range_match.group(1)
        )

        end = int(
            range_match.group(2)
        )

        if start <= 0 or end <= 0:
            return None

        if start < min_limit:
            return None

        if end < min_limit:
            return None

        if start > max_limit:
            return None

        if end > max_limit:
            return None

        if start > end:
            start, end = end, start

        return {
            "min": start,
            "max": end,
            "normalized": True
        }

    return None


# =====================================
# PRICE
# =====================================

def normalize_price(
    user_input: str
):

    original_input = (
        user_input
        .strip()
        .replace(" ", "")
    )

    if not original_input:
        return None

    if not original_input.isdigit():
        return None

    value = int(original_input)

    if value <= 0:
        return None

    if value > MAX_PRICE:
        return None

    return value


# =====================================
# READY HELPERS
# =====================================

def normalize_floor_range(
    user_input: str
):

    return normalize_range(
        user_input,
        min_limit=1,
        max_limit=MAX_FLOOR
    )


def normalize_area_range(
    user_input: str
):

    return normalize_range(
        user_input,
        min_limit=MIN_AREA,
        max_limit=MAX_AREA
    )