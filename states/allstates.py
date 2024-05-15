from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup
from bot.deploy import bot, botkey

class MyStates(StatesGroup):
    name = State()
    surname = State()
    age = State()

