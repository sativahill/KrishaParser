from aiogram.fsm.state import (
    StatesGroup,
    State
)


class ProfileStates(
    StatesGroup
):

    waiting_type = State()

    waiting_city = State()

    waiting_rooms = State()

    waiting_price = State()

    waiting_area = State()

    waiting_floor = State()