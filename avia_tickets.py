import json
from argparse import ArgumentParser
from datetime import datetime
import requests

#Код запускается из командной строки с аргументами описанными ниже
#Пример: python avia_tickets.py -o "Москва" -d "Нью-Йорк" -t "2019-07-30"

def create_parser():
    """Аргументы командной строки"""
    parser = ArgumentParser()
    parser.add_argument('-o', '--origin', default='Воронеж', type=str)
    parser.add_argument('-d', '--destination', default='Москва', type=str)
    parser.add_argument('-t', '--time', default=datetime.today().strftime('%Y-%m-%d'), type=str)
    return parser

def download_cities():
    """Скачаем json-файл IATA кодов городов"""
    url = "http://api.travelpayouts.com/data/ru/cities.json"
    with open('cities.json', 'wb') as file:
        data = requests.get(url)
        file.write(data.content)


def read_cities():
    """декодирование файла в текстовый формат и возврат json-объекта"""
    with open("cities.json", 'rb') as file:
        data = file.read()
    data = json.loads(data.decode('utf-8'))
    return data


def set_param(origin, destination, data_cities):
    """Возвращает flight parameters по имени города"""
    flight_param = {}
    for item in data_cities:
        if item["name"] == origin:
            flight_param["origin"] = item["code"]
        if item["name"] == destination:
            flight_param["destination"] = item["code"]
    return flight_param


def get_flight(origin, destination, depart_day, data_cities):
    """Итоговый запрос и вывод необходимой информации"""
    flight_params = set_param(origin, destination, data_cities)
    flight_params["depart_date"] = depart_day
    req = requests.get("http://min-prices.aviasales.ru/calendar_preload", flight_params)
    if req.status_code == 200:
        data = req.json()
        flights = data['current_depart_date_prices']
        for item in flights:
            print(f"Город вылета: {origin}\tНаправление: {destination}\tДата: {depart_day}\tЦена:{item['value']}\tГде купить: {item['gate']}")
    else:
        print(f'Что то пошло не так(')
        return


if __name__ == '__main__':

    try:
        with open("cities.json") as file:
            DATA = read_cities()
    except FileNotFoundError:                         #если файла нет
        download_cities()                             #то скачиваем
        DATA = read_cities()
    ARGS = create_parser().parse_args()
    get_flight(ARGS.origin, ARGS.destination, ARGS.time, DATA)


