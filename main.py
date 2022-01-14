import time
import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from DB_funcs import DB
from FSMstates import FSMmsg
from aptekaRu import aptekaRu
from SberEapteka import SberEapteka
from bot_config import tg_bot_token

def key_board():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Аптека.ру", "СберЕаптека",
               "Город", "Поиск аналогов"]
    keyboard.add(*buttons)
    return keyboard

FSM = FSMmsg()
DB = DB()
storage = MemoryStorage()
bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if DB.user_find(message.from_user.id) != True:
        DB.add_user(message.from_user.id)
    await message.answer('Привет! Напиши мне название лекарства и я попробую найти для него аналоги.', reply_markup=key_board())

@dp.message_handler(lambda message: "Город" in message.text, state=None)
async def get_city(message: types.Message):
    await FSM.city.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Вернуться назад')
    await message.reply('Введите город, в котором будет идти дальнейший поиск лекарств.', reply_markup=keyboard)
    if DB.search_city(message.from_user.id)[0] != None:
        await message.answer(f'Ваш город - {DB.search_city(message.from_user.id)[0]}.')

@dp.message_handler(state=FSM.city)
async def load_city(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться назад':
        await state.finish()
        await message.answer('Изменение города отменено.', reply_markup=key_board())
    else:
        DB.change_city(message.from_user.id, message.text)
        await state.finish()
        await message.answer('Город успешно добавлен!', reply_markup=key_board())

@dp.message_handler(lambda message: "Поиск аналогов" in message.text, state=None)
async def search_analogs(message: types.Message):
    if DB.search_city(message.from_user.id)[0] == None or DB.find_pharmacy(message.from_user.id)[0] == None:
        await message.answer('Перед тем, как начать поиск аналогов - введите город и выберите аптеку.', reply_markup=key_board())
    else:
        await FSM.search.set()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('Вернуться назад')
        await message.reply('Введите название препарата.', reply_markup=keyboard)

@dp.message_handler(state=FSM.search)
async def back_menu_from_search(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться назад':
        await state.finish()
        await message.answer('Поиск аналогов отменен.', reply_markup=key_board())
    else:
        try:
            if DB.find_pharmacy(message.from_user.id)[0] == 'СберЕаптека':
                msg = '\n'.join(SberEapteka(message.text, DB.search_city(message.from_user.id)[0]))          # объединение элементов массива в одну строку
            else:
                msg = '\n'.join(aptekaRu(message.text, DB.search_city(message.from_user.id)[0]))
            await message.answer(text=msg, reply_markup=key_board())
        except:
            await message.answer('Проверьте корректность ввода и попробуйте заново.', reply_markup=key_board())
        await state.finish()

@dp.message_handler(lambda message: ('Аптека.ру' in message.text) or ('СберЕаптека' in message.text))
async def change_apteka(message: types.Message):
    DB.change_pharmacy(user_id=message.from_user.id, Apteka=message.text)
    await message.answer('Аптека была изменена.')

@dp.message_handler(lambda message: 'Вернуться назад' in message.text)
async def return_to_menu(message: types.Message):
    await message.answer('Вы были возвращены в главное меню.', reply_markup=key_board())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

