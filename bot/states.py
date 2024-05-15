import telebot

from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup
import os
from telebot.storage import StateMemoryStorage # States storage

state_storage = StateMemoryStorage() # init state storage

botkey = os.getenv('FAC_BOT_TOKEN')
bot = telebot.TeleBot(botkey,
state_storage=state_storage)