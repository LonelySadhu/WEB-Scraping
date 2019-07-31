
import requests
from lxml import html

HEADER = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
           }
BASE_URL = 'https://hh.ru/search/vacancy'


def get_params(search_period=3, area=1, text='Программист Python', page=0):
    """search period: период появления вакансии,
       area:0 - Россия, 1 - Москва,
       text: необходимая вакансия,
       page: страница поиска"""
    params = {
        'search_period': search_period,
        'area': area,
        'text': text,
        'page': page
    }
    return params


def hh_parse(base_url, header):
    try:
        params = get_params()
        session = requests.Session()
        response = session.get(base_url, params=params, headers=header)
        if response.status_code == 200:
            page = html.fromstring(response.text)
            vacansion = page.xpath("//div[@class='vacancy-serp']//div//div//div//div//a/text()")
            vage = page.xpath("//div[@class='vacancy-serp-item__compensation']/text()")
            link = page.xpath("//div[@class='resume-search-item__name']/a/@href")

            for i in range(len(vage)):
                print(f'{vacansion[i]}\n{vage[i]}\n{link[i]}')
                print('--'*20)

        else:
            print(f'Bad response: {response.status_code}')

    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)


hh_parse(BASE_URL, HEADER)
