# states/admin.py
from aiogram.fsm.state import StatesGroup, State


class AdminAddDayStates(StatesGroup):
    waiting_for_date = State()
    waiting_for_times = State()


class AdminAddSlotStates(StatesGroup):
    waiting_for_date = State()
    waiting_for_time = State()


class AdminRemoveSlotStates(StatesGroup):
    waiting_for_date = State()
    waiting_for_choice = State()


class AdminCancelClientStates(StatesGroup):
    waiting_for_date = State()
    waiting_for_choice = State()


class AdminCloseDayStates(StatesGroup):
    waiting_for_date = State()


class AdminViewDayStates(StatesGroup):
    waiting_for_date = State()
