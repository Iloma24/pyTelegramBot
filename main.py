import dogapi.handlers
from bot.deploy import bot
import bot.handlers

if __name__ == '__main__':
    bot.deploy.bot.polling(none_stop=True) # bot's method setting the bot's mode. In this case - holding it in none-stop mode
    #bot.infinity_polling() # does the same thing as method 'bot.polling()'

