# this file is made to get random user data for further interaction with remote API
import requests

randomUserInfo = requests.get('https://randomuser.me/api/').text
