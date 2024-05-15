from bot.deploy import bot
import webbrowser

'''@bot.message_handler(commands=['start'])
def enterbreed(message):
    bot.send_message(message.chat.id, "Hi! Let's try to find out something new about dogs. \nEnter the name of the user_answer"
                                      " you are interested in!")'''

def goToLink(end_point=None):
    webbrowser.open('https://api.thedogapi.com/v1/breeds/search?q=air&attach_image={number}'.format(number=2))