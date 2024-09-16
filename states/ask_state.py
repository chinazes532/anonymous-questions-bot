from aiogram.fsm.state import State, StatesGroup


class AskState(StatesGroup):
    ask = State()