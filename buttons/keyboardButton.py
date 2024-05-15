from telebot import types # for adjusting the buttons settings
from bot.deploy import bot

@bot.message_handler() # if decorator has no parameter it will react any text entered by user in telegram even without '/'
def kbButton(message):
    keyb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton(text='button1')
    keyb.add(btn1)
    bot.send_message(message.chat.id, reply_markup=keyb)


def inlButton(message):
    keyb = types.InlineKeyboardMarkup(row_width=1)
    keyb.add(types.InlineKeyboardButton('button', callback_data='does something'),
             types.InlineKeyboardButton('button2', callback_data="doesn't do something" ))
    # another way to create 2 buttons - below:
    # keyb = types.InlineKeyboardMarkup(row_width=2)
    # button1 = types.InlineKeyboardButton('button', callback_data='doeas something')
    # button2 = types.InlineKeyboardButton('button2', callback_data="doesn't do something")
    # keyb.add(button1, button2)
    bot.send_message(message.chat.id, 'choose the option', reply_markup=keyb)


@bot.callback_query_handler(func=lambda call: True)
def did_or_not(call):
    if call.data == 'does something':
        bot.answer_callback_query(call.id, 'did something')
    elif call.data == "doesn't do something":
        bot.answer_callback_query(call.id, "didn't do something")

@bot.message_handler(func=lambda message: True)
def some_funct(message):
    bot.send_message(message.chat.id, "does/doesn't", reply_markup=did_or_not())
