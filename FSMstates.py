from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMmsg(StatesGroup):
    city = State()
    search = State()