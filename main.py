import requests
import ast
import os
import datetime
import random


def main():
    date_format = "%Y%m%d"
    now = datetime.date.today()
    authorization_code = open('authorization.txt', 'r')
    authorization_code = authorization_code.read()
    search = input('Where is the place you want to add to your recently visited? ')
    location = input('Where are you? ')
    url = 'https://api.yelp.com/v3/businesses/search?term=' + search + '&location=' + location
    r = requests.get(url,
        headers = {
            'Authorization': authorization_code
        }
    )

    new = r.json()
    print('Choose the location:')
    for i in range(len(new['businesses'])):
        print('[' + str(i) + ']' + new['businesses'][i]['name'] + ' - ' + new['businesses'][i]['location']['address1'])

    index = input()
    index = int(index)

    new_place = {
        new['businesses'][index]['name']: {
            "link": new['businesses'][index]['url'],
            "name": new['businesses'][index]['name'],
            "categories": new['businesses'][index]['categories'],
            "last visit": now.strftime(date_format),
            "time weight": 0,
            "categories weight": 0,
            "total weight": 0
        }
    }

    update_categories(new_place, new['businesses'][index]['name'])

    with open('places.txt') as f:
        data = ast.literal_eval(f.read())

    f = open('places.txt', 'w+')

    data.update(new_place)

    f.write(str(data))

    print('\n'.join(map(str, data)))


def update_entries():
    date_format = "%Y%m%d"
    now = datetime.date.today()

    with open('places.txt') as f:
        places = ast.literal_eval(f.read())

    with open('categories.txt') as f:
        categories = ast.literal_eval(f.read())

    f = open('places.txt', 'w+')

    for key in places.items():
        delta = now - datetime.datetime.strptime(places[key[0]]['last visit'], date_format).date()
        places[key[0]]['time weight'] = int(delta.days / 7)
        places[key[0]]['categories weight'] = 0

        for item in places[key[0]]['categories']:
            deltac = now - datetime.datetime.strptime(categories[item['alias']]['last visited'], date_format).date()
            places[key[0]]['categories weight'] += int(deltac.days / 7)

        places[key[0]]['total weight'] = places[key[0]]['categories weight'] + places[key[0]]['time weight']

    f.write(str(places))


def update_categories(place, place_key):
    date_format = "%Y%m%d"
    now = datetime.date.today()

    with open('categories.txt') as f:
        data = ast.literal_eval(f.read())

    for item in place[place_key]['categories']:
        category = {
            item['alias']: {
                "last visited": now.strftime(date_format)
            }
        }
        data.update(category)

    f = open('categories.txt', 'w+')
    f.write(str(data))


def choose_existing():
    weighted_list = []
    i = 0

    with open('places.txt') as f:
        data = ast.literal_eval(f.read())

    for key in data.items():
        weighted_list[i:] = [data[key[0]]['name']] * (int(data[key[0]]['time weight']))
        i += int(data[key[0]]['time weight'])

    print(random.choice(weighted_list))


def file_check():
    if not os.path.exists('places.txt') or os.path.getsize('places.txt') == 0:
        f = open('places.txt', 'w+')
        f.write('{}')
        f.close()

    if not os.path.exists('categories.txt') or os.path.getsize('categories.txt') == 0:
        f = open('categories.txt', 'w+')
        f.write('{}')
        f.close()


if __name__ == "__main__":
    press = input('Test adding location press 1, test updating press 2: \n')
    file_check()
    if press == '1':
        main()
    if press == '2':
        update_entries()
    if press == '3':
        choose_existing()
