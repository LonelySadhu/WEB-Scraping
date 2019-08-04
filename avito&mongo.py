import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

BASE_URL = "https://www.avito.ru/moskva"

def get_params(whats_find, page=None):

    params = {
        'q': whats_find,
        'p': page
    }
    return params


def request_to_avito(url, params):
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.text
        else:
            print('Bad response!')
            exit(1)
    except response.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)

def get_page_data(text_response):
    soup = BeautifulSoup(text_response, 'html.parser')
    items = soup.find_all('div', {'class': 'item__line'})
    for item in items:
        category = item.find('div', {'class': 'data'}).get_text()
        category = re.findall(r"[А-Я]?[а-я]+\s[и]?\s?[а-яА-Я]*\s?[а-яА-Я]*", category)
        category = category[0] if category else 'unnamed category'
        title = item.find('span', {'itemprop': 'name'}).string
        price = item.find('span', {'class': 'price', 'itemprop': 'price'}).text
        price = re.findall(r"[\d]+\s[\d]+", price)
        price = price[0].replace(' ', '') if price else 'Цена не указана'
        location_data = item.find('div', {'class': 'data'}).get_text()
        metro = re.findall(r"[м]+\.\s[а-яА-Я]+\S*[а-яА-Я]*", location_data)
        metro = metro[0] if metro else 'место не указано'
        link = item.find('a', {'class': 'item-description-title-link'})['href']
        link = 'https://www.avito.ru'+link
        data = {
            'category': category,
            'title': title,
            'price': price,
            'metro': metro,
            'link': link
        }
        save_to_mongo(data)


def save_to_mongo(data):
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.avito
    category = data['category']
    collection = db[f'{category}']
    if collection.find_one(data) == data:  #Добавляем только новые объявления
        pass
    else:
        collection.insert_one(data)



params = get_params('xiaomi')
response = request_to_avito(BASE_URL, params)
get_page_data(response)


