import random
import asyncio


USER_AGENTS = [
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
]


def get_random_user_agent():
    return random.choice(USER_AGENTS)


async def random_delay(min_sec: int, max_sec: int):
    delay = random.uniform(min_sec, max_sec)
    await asyncio.sleep(delay)