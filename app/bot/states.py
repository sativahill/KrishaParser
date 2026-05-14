from aiogram.fsm.state import (
    StatesGroup,
    State
)


class ProfileStates(
    StatesGroup
):

    waiting_city = State()

    waiting_rooms = State()

    waiting_price = State()