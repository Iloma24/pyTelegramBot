import pprint
import sqlite3
import requests # library for making requests to the sites
import json # library for converting strings to json files
import os

apikey = os.getenv('DOG_API_KEY') # hidden information in .env file (API key of the site)
param = {'key': apikey}
name = 'boxer'
all_breeds_data_link = 'https://api.thedogapi.com/v1/breeds'
breeds_searching = 'https://api.thedogapi.com/v1/images/search?limit=10&breed_ids=Akita&api_key={REPLACE_ME}'.format(REPLACE_ME=apikey)
#get_images = 'https://api.thedogapi.com/v1/images/{images_id}'.format(images_id=images_id)
total = requests.get('https://api.thedogapi.com/v1/breeds?limit=180&page=0').json()
all_info = requests.get(all_breeds_data_link).json()
all_breeds_data = dict()
for elem in all_info:
    all_breeds_data[elem['name']] = elem
# with open('all_data.txt', 'w') as file:
#     json.dump(all_info, file, indent=4)

#pprint.pprint(all_info)
x = requests.get('https://api.thedogapi.com/v1/images/search?limit=10&breed_ids=beng&api_key={REPLACE_ME}'.format(REPLACE_ME=apikey))
y = requests.get('https://api.thedogapi.com/v1/images/search?breed_ids=111')
resp2 = requests.get('https://api.thedogapi.com/v1/images/search?id=1').json()
#print(resp2)
