from aiogram.fsm.state import State, StatesGroup


class CallbackAskState(StatesGroup):
    callback_ask = State()