import requests
import pprint # library for pretty looking dictionaries
from dogapiData import main_url
from userData import randomUserInfo # personal local module with random user data for headers requests


def breeds():
    resp = requests.get('https://api.thedogapi.com/v1/breeds')
    resp_json = resp.json()
    pprint.pprint(resp_json)


def siteHeaders():
    resp = requests.get(main_url)
    sHeaders = resp.headers
    pprint.pprint(sHeaders)


def clientHeaders():
    resp = requests.get(main_url)
    print(resp.request.headers)

#siteHeaders()
#clientHeaders()
#userInfo = userData.randomUserInfo
#print(userInfo)