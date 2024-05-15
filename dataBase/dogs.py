import json
import pprint
import sqlite3
import requests
from dogapi.dogapiData import all_breeds_data

with sqlite3.connect('bases.db') as conn:
    curs = conn.cursor()
    curs.execute('CREATE TABLE IF NOT EXISTS dogs_table ('
                     'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                     'bred_for VARCHAR,'
                     'breed_group VARCHAR,'
                     'height INTEGER,'
                     'weight INTEGER'
                     'breed_id INTEGER,'
                     'life_span VARCHAR,'
                     'name VARCHAR,'
                     'origin VARCHAR,'
                     'temperament TEXT,'
                     'description TEXT,'
                     'history TEXT)')
    conn.commit()

data_from_server = requests.get('https://api.thedogapi.com/v1/breeds')
text_data_server = json.loads(data_from_server.text)
#pprint.pprint(data_from_server.json())
# with open('breedsNames.txt', 'w') as bn_file:
#     for elem in all_breeds_data:
#         bn_file.writelines(f'{elem}\n')

# for elem in data_from_server.json():
#     if not 'bred_for' in elem.keys():
#         elem['bred_for'] = 'no information'
#         print(elem)


'''with sqlite3.connect('bases.db') as conn:
    curs = conn.cursor()
    for elem in all_breeds_data:
        if not 'bred_for' in elem.keys():
            elem.setdefault('bred_for', 'No information')
        if not 'breed_id' in elem.keys():
            elem.setdefault('breed_id', 'No information')
        if not 'description' in elem.keys():
            elem.setdefault('description', 'No information')
        if not 'history' in elem.keys():
            elem.setdefault('history', 'No information')
        curs.execute("INSERT INTO dogs_table (bred_for, breed_group, height, weight, breed_id, life_span, name, origin,"
                     f"temperament, description, history) VALUES (f'{elem['bred_for']}, {elem['breed_group']}, "
                     f"{elem['height']['metric']}, {elem['weight']['metric']}, {elem['id']}, {elem['life_span']}, "
                     f"{elem['name']}, {elem['origin']}, {elem['temperament']}, {elem['description']}, {elem['history']}')")'''


with sqlite3.connect('bases.db') as conn:
    curs = conn.cursor()
    for elem in data_from_server.json():
        if not 'bred_for' in elem.keys() or elem['bred_for'] == '':
            elem['bred_for'] = 'No information'
        if not 'breed_id' in elem.keys() or elem['breed_id'] == '':
            elem['breed_id'] = 'No information'
        if not 'description' in elem.keys() or elem['description'] == '':
            elem['description'] = 'No information'
        if not 'history' in elem.keys() or elem['history'] == '':
            elem['history'] = 'No information'
        curs.execute(f"INSERT INTO dogs_table (bred_for, breed_group, height, weight, breed_id, life_span, name, origin,"
                     f"temperament, description, history) VALUES ({elem['bred_for']}, {elem['breed_group']}, "
                     f"{elem['height']['metric']}, {elem['weight']['metric']}, {elem['id']}, {elem['life_span']}, "
                     f"{elem['name']}, {elem['origin']}, {elem['temperament']}, {elem['description']}, {elem['history']})")


