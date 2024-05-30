import random
import sqlite3

from random import choice
import json
import pprint
import requests
from telebot import types # for adjusting the buttons settings
from dogapi.dogapiData import all_breeds_data, all_info
import dogapi.handlers
from bot.deploy import bot
from bot import commands


data_for_searching = {'name': None, 'bred for': None, 'breed group': None}
user_choice = None
list_of_breeds = [x for x in all_breeds_data.keys()]
user_answer = None
name_of_breed = None # global variable contains name of the name_of_breed
images_id = None # global variable contains image id
breed_id = None # global variable contains id of the name_of_breed
images_link = requests.get(f'https://api.thedogapi.com/v1/images/search?breed_id={breed_id}').json()
respons_for_user = {'weight': 'no information', 'height': 'no information', 'bred for': 'no information',
                    'breed group': 'no information', 'life span': 'no information',
                    'temperament': 'no information', 'origin': 'no information', 'description': 'no information',
                    'history': 'no information'}


@bot.message_handler(commands=['start']) # decorator contains the list of commands on which bot have to
                                                        # react. Commands in telegram must start with '/'
def general(message): # func gets one parameter "message" that contains all information about user connecting with bot.
                    # Also all information about current chat
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    but1 = types.KeyboardButton('Yes'.lower())
    but2 = types.KeyboardButton('No'.lower())
    buttons.add(but1, but2)
    bot.send_message(message.chat.id, f'Hi {message.from_user.first_name}! \nWould you like to know something new about dogs?'
                                      f'\nPress - "yes" or "no"', reply_markup=buttons)
    bot.register_next_step_handler(message, yes_or_no)


def yes_or_no(message):
    if message.text == 'Yes' or message.text == 'yes':
        breed_name = bot.send_message(message.chat.id, 'enter the name of the name_of_breed you want to know about')
        bot.register_next_step_handler(breed_name, get_info_from_table)
    elif message.text == 'No' or message.text == 'no':
        bot.send_message(message.chat.id, 'OK, you can call me any time!')
    else:
        repeat = bot.send_message(message.chat.id, 'Incorrect input, type any letter!')
        bot.register_next_step_handler(repeat, new_search)


def get_info_from_table(message):
    global data_for_searching
    global respons_for_user
    data_for_searching['name'] = message.text.title()
    images_link = None
    with sqlite3.connect(r'D:\Skillbox\projects\telegramBot\bases.db') as conn:
        curs = conn.cursor()
        table_for_loop = curs.execute('SELECT * FROM dogs_table')
        for column in table_for_loop:
            if data_for_searching['name'] in column[7]:
                respons_for_user['weight'] = column[4]
                respons_for_user['height'] = column[3]
                respons_for_user['bred for'] = column[1]
                respons_for_user['breed group'] = column[2]
                respons_for_user['life span'] = column[6]
                respons_for_user['temperament'] = column[9]
                respons_for_user['origin'] = column[8]
                respons_for_user['description'] = column[10]
                respons_for_user['history'] = column[11]
                images_link = f'https://cdn2.thedogapi.com/images/{column[12]}.jpg'
        responses1 = [f"Hm {data_for_searching['name']}, interesting choice!", "Voila!", "Get it!", "Done", "That's it!", "WOW"]
        bot.send_message(message.chat.id, f'{random.choice(responses1)}')
        bot.send_message(message.chat.id, f'That is what I know about {data_for_searching["name"]}.'
                                          f'\nweight: {respons_for_user["weight"]} kg.;'
                                          f'\nheight: {respons_for_user["height"]} cm.;'
                                          f'\nbred for: {respons_for_user["bred for"]};'
                                          f'\nbreed group: {respons_for_user["breed group"]};'
                                          f'\nlife span: {respons_for_user["life span"]};'
                                          f'\ntemperament: {respons_for_user["temperament"]};'
                                          f'\norigin: {respons_for_user["origin"]};'
                                          f'\ndescription: {respons_for_user["description"]};'
                                          f'\nhistory: {respons_for_user["history"]}.')
        buttons = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton('watch photo', url=images_link)
        but2 = types.InlineKeyboardButton('Show all breeds names', callback_data='all breeds names')
        buttons.add(but1, but2)
        bot.send_message(message.chat.id, 'if you want to see the photo, click "watch photo", '
                                          'or you can see all breeds names', reply_markup=buttons)
        # new_search = bot.send_message(message.chat.id, 'Would you like to try again? Enter yes/no')
        # bot.register_next_step_handler(new_search, yes_or_no)




'''def yes_or_no(message):
    elif message.text == 'Yes' or message.text == 'yes':
        # breed_name = bot.send_message(message.chat.id, 'choose one of the option, '
        #                                                '\nor enter the name of the name_of_breed you want to know about')
        buttons = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton('All types of breeds', callback_data='all types of breeds')
        but2 = types.InlineKeyboardButton('Show all breeds names', callback_data='all breeds names')
        but3 = types.InlineKeyboardButton('Bred for', callback_data='bred for')
        buttons.add(but1, but2, but3, row_width=2)
        bot.send_message(message.chat.id, 'choose one of the option, '
                              '\nor enter the name of the breed you want to know about', reply_markup=buttons)
    else:
        repeat = bot.send_message(message.chat.id, 'Incorrect input, type any letter!')
        bot.register_next_step_handler(repeat, general)'''

@bot.callback_query_handler(func=lambda choice: True)
def callback_handler_first_choice(choice):
    with sqlite3.connect(r'D:\Skillbox\projects\telegramBot\bases.db') as conn:
        curs = conn.cursor()
        table_for_loop = curs.execute('SELECT * FROM dogs_table')
        reaction_on_but = ''
        for elem in table_for_loop:
            if choice.data == 'all breeds names':
                if str(elem[7]) not in reaction_on_but and str(elem[7]) != 'No information':
                    reaction_on_but += f'{str(elem[7])}\n'
                    bot.send_message(choice.message.chat.id, f'{reaction_on_but} \nto begin searching type - "/start"')


def new_search(message):
    if message.text:
        breed_name = bot.send_message(message.chat.id, 'enter the name of the breed you want to know about')
        bot.register_next_step_handler(breed_name, get_info_from_table)


'''def get_info_from_table(message):
    with sqlite3.connect('bases.db') as conn:
        curs = conn.cursor()
        global name_of_breed
        name_of_breed = message.text.title()
        flag = None
        for one_breed_data in all_breeds_data:
            if name_of_breed in one_breed_data:
                flag = True
                name_of_breed = one_breed_data
                break
            else:
                flag = False
        if flag == False:
            bot.send_message(message.chat.id, 'there is no such a name_of_breed')
        # if name_of_breed not in all_breeds_data:
        #     bot.send_message(message.chat.id, 'there is no such a name_of_breed')

        else:
            with sqlite3.connect('bases.db') as conn:
                curs = conn.cursor()
                curs.execute('SELECT ')
        get_images = f'https://cdn2.thedogapi.com/images/{images_id}.jpg'
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('watch photo', url=get_images)
        markup.add(btn1)
        bot.send_message(message.chat.id, 'if you want to see the photo, click "watch photo"', reply_markup=markup)
    new_search = bot.send_message(message.chat.id, 'Would you like to try again? yes/no')
    bot.register_next_step_handler(new_search, yes_or_no)'''



# works without using table dogs_table
'''def get_breed(message):
    global user_answer
    global images_id
    global respons_for_user
    global name_of_breed
    name_of_breed = message.text.title()
    # version 1
    flag = None
    for one_breed_data in all_breeds_data:
        if name_of_breed in one_breed_data:
            flag = True
            name_of_breed = one_breed_data
            break
        else:
            flag = False
    if flag == False:
        bot.send_message(message.chat.id, 'there is no such a name_of_breed')
    # if name_of_breed not in all_breeds_data:
    #     bot.send_message(message.chat.id, 'there is no such a name_of_breed')

    else:
        for elem in all_info:
            if elem['name'] == name_of_breed:
                respons_for_user['weight'] = elem["weight"]["metric"] if 'weight' in elem.keys() else 'no information'
                respons_for_user['height'] = elem["height"]["metric"] if 'height' in elem.keys() else 'no information'
                respons_for_user['bred for'] = elem["bred_for"] if 'bred_for' in elem.keys() else 'no information'
                respons_for_user['name_of_breed group'] = elem["breed_group"] if 'breed_group' in elem.keys() else 'no information'
                respons_for_user['life span'] = elem["life_span"] if 'life_span' in elem.keys() else 'no information'
                respons_for_user['temperament'] = elem["temperament"] if 'temperament' in elem.keys() else 'no information'
                respons_for_user['origin'] = elem["origin"] if 'origin' in elem.keys() else 'no information'
                respons_for_user['description'] = elem["description"] if 'description' in elem.keys() else 'no information'
                respons_for_user['history'] = elem["history"] if 'history' in elem.keys() else 'no information'
                images_id = elem['reference_image_id']
        responses1 = [f'Hm "{name_of_breed}" interesting choice!', 'Get it!', 'Done', "That's it!", 'WOW']
        bot.send_message(message.chat.id, f'{random.choice(responses1)}')
        bot.send_message(message.chat.id, f'That is what I know about {name_of_breed}.'
                                          f'\nweight: {respons_for_user["weight"]} kg.'
                                          f'\nheight: {respons_for_user["height"]} cm. '
                                          f'\nbred for: {respons_for_user["bred for"]} '
                                          f'\nname_of_breed group: {respons_for_user["name_of_breed group"]} '
                                          f'\nlife span: {respons_for_user["life span"]} '
                                          f'\ntemperament: {respons_for_user["temperament"]}'
                                          f'\norigin: {respons_for_user["origin"]}'
                                          f'\ndescription: {respons_for_user["description"]}'
                                          f'\nhistory: {respons_for_user["history"]}')


        # version 2 doesn't work correctly
        # bot.send_message(message.chat.id, f'Hm "{name_of_breed}" interesting choice!')
        # bot.send_message(message.chat.id, f'That is what I know about {name_of_breed}.'
        #                                   f'\nweight: {all_breeds_data[name_of_breed]["weight"]["metric"]} kg.'
        #                                   f'\nheight: {all_breeds_data[name_of_breed]["height"]["metric"]} cm. '
        #                                   f'\nbred for: {all_breeds_data[name_of_breed]["bred_for"]} '
        #                                   f'\nname_of_breed group: {all_breeds_data[name_of_breed]["breed_group"]} '
        #                                   f'\nlife span: {all_breeds_data[name_of_breed]["life_span"]} '
        #                                   f'\ntemperament: {all_breeds_data[name_of_breed]["temperament"]}')


        # version 3 doesn't work
        # bot.send_message(message.chat.id, f'Hm "{name_of_breed}" interesting choice!')
        # try:
        #     bot.send_message(message.chat.id, f'That is what I know about {name_of_breed}.'
        #                                       f'\nweight: {all_breeds_data[name_of_breed]["weight"]["metric"]} kg.'
        #                                       f'\nheight: {all_breeds_data[name_of_breed]["height"]["metric"]} cm. '
        #                                       f'\nbred for: {all_breeds_data[name_of_breed]["bred_for"]} '
        #                                       f'\nname_of_breed group: {all_breeds_data[name_of_breed]["breed_group"]} '
        #                                       f'\nlife span: {all_breeds_data[name_of_breed]["life_span"]} '
        #                                       f'\ntemperament: {all_breeds_data[name_of_breed]["temperament"]}'
        #                                       f'\norigin: {all_breeds_data[name_of_breed]["origin"]}'
        #                                       f'\ndescription: {all_breeds_data[name_of_breed]["description"]}'
        #                                       f'\nhistory: {all_breeds_data[name_of_breed]["history"]}')
        # except KeyError as exc:
        #     bot.send_message(message.chat.id, f'{exc}: no information')


        # version 4 works
        # try:
        #     bot.send_message(message.chat.id, f'\nweight: {all_breeds_data[name_of_breed]["weight"]["metric"]} kg.')
        # except KeyError as exc:
        #     bot.send_message(message.chat.id, f'{exc}: no information')
        # try:
        #     bot.send_message(message.chat.id, f'\nheight: {all_breeds_data[name_of_breed]["height"]["metric"]} cm. ')
        # except KeyError as exc:
        #         bot.send_message(message.chat.id, f'{exc}: no information')
        # try:
        #     bot.send_message(message.chat.id, f'\nbred for: {all_breeds_data[name_of_breed]["bred_for"]} ')
        # except KeyError as exc:
        #     bot.send_message(message.chat.id, f'{exc}: no information')
        # try:
        #     bot.send_message(message.chat.id, f'\nname_of_breed group: {all_breeds_data[name_of_breed]["breed_group"]} ')
        # except KeyError as exc:
        #     bot.send_message(message.chat.id, f'{exc}: no information')
        # try:
        #     bot.send_message(message.chat.id, f'\nlife span: {all_breeds_data[name_of_breed]["life_span"]} ')
        # except KeyError as exc:
        #         bot.send_message(message.chat.id, f'{exc}: no information')
        # try:
        #     bot.send_message(message.chat.id, f'\ntemperament: {all_breeds_data[name_of_breed]["temperament"]}')
        # except KeyError as exc:
        #     bot.send_message(message.chat.id, f'{exc}: no information')
        # try:
        #     bot.send_message(message.chat.id, f'\norigin: {all_breeds_data[name_of_breed]["origin"]}')
        # except KeyError as exc:
        #     bot.send_message(message.chat.id, f'{exc}: no information')
        # try:
        #     bot.send_message(message.chat.id, f'\ndescription: {all_breeds_data[name_of_breed]["description"]}')
        # except KeyError as exc:
        #         bot.send_message(message.chat.id, f'{exc}: no information')
        # try:
        #     bot.send_message(message.chat.id, f'\nhistory: {all_breeds_data[name_of_breed]["history"]}')
        # except KeyError as exc:
        #     bot.send_message(message.chat.id, f'{exc}: no information')
        # global images_id
        # images_id = all_breeds_data[name_of_breed]["reference_image_id"]
        get_images = f'https://cdn2.thedogapi.com/images/{images_id}.jpg'
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('watch photo', url=get_images)
        markup.add(btn1)
        bot.send_message(message.chat.id, 'if you want to see the photo, click "watch photo"', reply_markup=markup)
    new_search = bot.send_message(message.chat.id, 'Would you like to try again? yes/no')
    bot.register_next_step_handler(new_search, yes_or_no)'''


'''@bot.callback_query_handler(func=lambda callback: True) # handler for button 'btn1'
def btn1Func(callback):
    if callback.data == 'edit':
        bot.edit_message_text('edited message', callback.message.chat.id, callback.message.message_id-1) # 'message_id-1'
        # means that it would be edited penultimate message'''

# if you need to create inline button outside the handler
'''markup = types.InlineKeyboardMarkup()
markup.add(types.InlineKeyboardButton('Open the link', url='https://www.thedogapi.com/'))
bot.send_message(chat_id=1302755310, text='have a nice time!', reply_markup=markup)'''

# if you need to create keyboard button outside the handler
'''markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('a')
itembtn2 = types.KeyboardButton('b')
itembtn3 = types.KeyboardButton('c')
markup.add(itembtn1, itembtn2, itembtn3)
bot.send_message(chat_id=1302755310, text='choose the letter', reply_markup=markup)'''

@bot.message_handler(commands=['info'])
def getUserInfo(message): # func returns all info about user presented in variable 'message'
    bot.send_message(message.chat.id, message)


'''@bot.message_handler()
def get_menu(message):
    if message.text == 'menu'.strip().lower():
        bot.register_next_step_handler(message, general)'''


'''@bot.message_handler(func=lambda message: True)
def echo_all(message): # this func reacts to all the rest commands except those are in func 'general'
    bot.reply_to(message, 'Please choose one of the offered comands!') # does the same thing as method 'bot.send_message()'
#    bot.reply_to(message, message.text)
'''

'''@bot.message_handler() # if decorator has no parameter it will react any text entered by user in telegram even without '/'
def general_second(message):
    if message.text.lower() == 'привет': # if entered specified word
       return bot.send_message(message.chat.id, f'Hi {message.from_user.first_name}!')
    bot.send_message(message.chat.id, 'specify your request please!')'''
