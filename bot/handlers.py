import random

from random import choice
import json
import pprint
import requests
from telebot import types # for adjusting the buttons settings
from dogapi.dogapiData import all_breeds_data, all_info
import dogapi.handlers
from bot.deploy import bot


list_of_breeds = [x for x in all_breeds_data.keys()]
user_answer = None
breed = None # global variable contains name of the breed
images_id = None # global variable contains image id
breed_id = None # global variable contains id of the breed
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


# @bot.message_handler(commands=['show all breeds'])
# def sab(message):
#     global list_of_breeds
#     bot.send_message(message.chat.id, list_of_breeds)
#     bot.send_message(message.chat.id, 'to start searching choose option "start" in "menu" block')


def yes_or_no(message):
    if message.text == 'Yes' or message.text == 'yes':
        breed_name = bot.send_message(message.chat.id, 'enter the name of the breed you want to know about')
        bot.register_next_step_handler(breed_name, get_breed)
    elif message.text == 'No' or message.text == 'no':
        bot.send_message(message.chat.id, 'OK, you can call me any time!')


# def new_search(message):
#     global user_answer
#     if user_answer == 'Yes' or 'yes':
#         breed_name = bot.send_message(message.chat.id, 'enter the name of the breed you want to know about')
#         bot.register_next_step_handler(breed_name, get_breed)
#     elif user_answer == 'No' or 'no':
#         bot.send_message(message.chat.id, 'OK, you can call me any time!')


def get_breed(message):
    global user_answer
    global images_id
    global respons_for_user
    global breed
    breed = message.text.title()
    # version 1
    flag = None
    for br in all_breeds_data:
        if breed in br:
            flag = True
            breed = br
            break
        else:
            flag = False
    if flag == False:
        bot.send_message(message.chat.id, 'there is no such a breed')
    # if breed not in all_breeds_data:
    #     bot.send_message(message.chat.id, 'there is no such a breed')

    else:
        for elem in all_info:
            if elem['name'] == breed:
                respons_for_user['weight'] = elem["weight"]["metric"] if 'weight' in elem.keys() else 'no information'
                respons_for_user['height'] = elem["height"]["metric"] if 'height' in elem.keys() else 'no information'
                respons_for_user['bred for'] = elem["bred_for"] if 'bred_for' in elem.keys() else 'no information'
                respons_for_user['breed group'] = elem["breed_group"] if 'breed_group' in elem.keys() else 'no information'
                respons_for_user['life span'] = elem["life_span"] if 'life_span' in elem.keys() else 'no information'
                respons_for_user['temperament'] = elem["temperament"] if 'temperament' in elem.keys() else 'no information'
                respons_for_user['origin'] = elem["origin"] if 'origin' in elem.keys() else 'no information'
                respons_for_user['description'] = elem["description"] if 'description' in elem.keys() else 'no information'
                respons_for_user['history'] = elem["history"] if 'history' in elem.keys() else 'no information'
                images_id = elem['reference_image_id']
        responses1 = [f'Hm "{breed}" interesting choice!', 'Get it!', 'Done', "That's it!"]
        bot.send_message(message.chat.id, f'{random.choice(responses1)}')
        bot.send_message(message.chat.id, f'That is what I know about {breed}.'
                                          f'\nweight: {respons_for_user["weight"]} kg.'
                                          f'\nheight: {respons_for_user["height"]} cm. '
                                          f'\nbred for: {respons_for_user["bred for"]} '
                                          f'\nbreed group: {respons_for_user["breed group"]} '
                                          f'\nlife span: {respons_for_user["life span"]} '
                                          f'\ntemperament: {respons_for_user["temperament"]}'
                                          f'\norigin: {respons_for_user["origin"]}'
                                          f'\ndescription: {respons_for_user["description"]}'
                                          f'\nhistory: {respons_for_user["history"]}')


        # version 2 doesn't work correctly
        # bot.send_message(message.chat.id, f'Hm "{breed}" interesting choice!')
        # bot.send_message(message.chat.id, f'That is what I know about {breed}.'
        #                                   f'\nweight: {all_breeds_data[breed]["weight"]["metric"]} kg.'
        #                                   f'\nheight: {all_breeds_data[breed]["height"]["metric"]} cm. '
        #                                   f'\nbred for: {all_breeds_data[breed]["bred_for"]} '
        #                                   f'\nbreed group: {all_breeds_data[breed]["breed_group"]} '
        #                                   f'\nlife span: {all_breeds_data[breed]["life_span"]} '
        #                                   f'\ntemperament: {all_breeds_data[breed]["temperament"]}')


        # version 3 doesn't work
        # bot.send_message(message.chat.id, f'Hm "{breed}" interesting choice!')
        # try:
        #     bot.send_message(message.chat.id, f'That is what I know about {breed}.'
        #                                       f'\nweight: {all_breeds_data[breed]["weight"]["metric"]} kg.'
        #                                       f'\nheight: {all_breeds_data[breed]["height"]["metric"]} cm. '
        #                                       f'\nbred for: {all_breeds_data[breed]["bred_for"]} '
        #                                       f'\nbreed group: {all_breeds_data[breed]["breed_group"]} '
        #                                       f'\nlife span: {all_breeds_data[breed]["life_span"]} '
        #                                       f'\ntemperament: {all_breeds_data[breed]["temperament"]}'
        #                                       f'\norigin: {all_breeds_data[breed]["origin"]}'
        #                                       f'\ndescription: {all_breeds_data[breed]["description"]}'
        #                                       f'\nhistory: {all_breeds_data[breed]["history"]}')
        # except KeyError as exc:
        #     bot.send_message(message.chat.id, f'{exc}: no information')


        # version 4 works
        # try:
        #     bot.send_message(message.chat.id, f'\nweight: {all_breeds_data[breed]["weight"]["metric"]} kg.')
        # except KeyError as exc:
        #     bot.send_message(message.chat.id, f'{exc}: no information')
        # try:
        #     bot.send_message(message.chat.id, f'\nheight: {all_breeds_data[breed]["height"]["metric"]} cm. ')
        # except KeyError as exc:
        #         bot.send_message(message.chat.id, f'{exc}: no information')
        # try:
        #     bot.send_message(message.chat.id, f'\nbred for: {all_breeds_data[breed]["bred_for"]} ')
        # except KeyError as exc:
        #     bot.send_message(message.chat.id, f'{exc}: no information')
        # try:
        #     bot.send_message(message.chat.id, f'\nbreed group: {all_breeds_data[breed]["breed_group"]} ')
        # except KeyError as exc:
        #     bot.send_message(message.chat.id, f'{exc}: no information')
        # try:
        #     bot.send_message(message.chat.id, f'\nlife span: {all_breeds_data[breed]["life_span"]} ')
        # except KeyError as exc:
        #         bot.send_message(message.chat.id, f'{exc}: no information')
        # try:
        #     bot.send_message(message.chat.id, f'\ntemperament: {all_breeds_data[breed]["temperament"]}')
        # except KeyError as exc:
        #     bot.send_message(message.chat.id, f'{exc}: no information')
        # try:
        #     bot.send_message(message.chat.id, f'\norigin: {all_breeds_data[breed]["origin"]}')
        # except KeyError as exc:
        #     bot.send_message(message.chat.id, f'{exc}: no information')
        # try:
        #     bot.send_message(message.chat.id, f'\ndescription: {all_breeds_data[breed]["description"]}')
        # except KeyError as exc:
        #         bot.send_message(message.chat.id, f'{exc}: no information')
        # try:
        #     bot.send_message(message.chat.id, f'\nhistory: {all_breeds_data[breed]["history"]}')
        # except KeyError as exc:
        #     bot.send_message(message.chat.id, f'{exc}: no information')
        # global images_id
        # images_id = all_breeds_data[breed]["reference_image_id"]
        get_images = f'https://cdn2.thedogapi.com/images/{images_id}.jpg'
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('watch photo', url=get_images)
        markup.add(btn1)
        bot.send_message(message.chat.id, 'if you want to see the photo, push "watch photo"', reply_markup=markup)
    new_search = bot.send_message(message.chat.id, 'Would you like to try again? yes/no')
    bot.register_next_step_handler(new_search, yes_or_no)

s = 'Caucasian Shepherd'
f = 'Puli'
marker = None
#print(s in all_breeds_data)
# for elem in list_of_breeds:
#     if s in elem:
#         marker = True
# print(marker)


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
