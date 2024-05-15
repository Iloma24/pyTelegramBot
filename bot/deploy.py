import telebot # one of the libraries to create telegram bot
import os # library to work with computer operational system
from dotenv import load_dotenv # library working with environmental variables
from telebot.storage import StateMemoryStorage

stateStorage = StateMemoryStorage()
load_dotenv() # allows to call environmental variables containing confidential information
botkey = os.getenv('FAC_BOT_TOKEN') # bot token
bot = telebot.TeleBot(botkey) # creation of the bot itself