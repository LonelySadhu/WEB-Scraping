import requests
from bs4 import BeautifulSoup
import re


def request_to_yandex():
    header = {
        'accept': '*/*',
         'user-agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }

    try:
        response = requests.get('https://news.yandex.ru/Moscow', headers=header)
        return response.text
    except response.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)


def news_parsing():
    html_doc = request_to_yandex()
    soup = BeautifulSoup(html_doc, 'html.parser')
    rubric_label = soup.find_all('a', {'class': 'rubric-label'})
    rubric_list = set()
    for rubric in rubric_label:
        rubric_list.add(rubric.get_text())
    rubric_list = list(rubric_list)
    articles = soup.find_all('div', {'class': 'story'})
    for category in rubric_list:
        print('Category:', category, '\n', '/\\' * 40)
        for article in articles:
            try:
                if article.find(class_=re.compile('rubric-label')).get_text() == category:
                    print('Title:')
                    print(article.find('h2', {'class': 'story__title'}).get_text())
                    print('Text:')
                    try:
                        print(article.find('div', {'class': 'story__text'}).get_text())
                    except AttributeError:
                        print('News contains only title')
                        print('--' * 20)
                    print('https://news.yandex.ru'+article.find('a', {'class': 'link_theme_black'})['href']).lstrip('/story')
                    print(article.find('div', {'class': 'story__date'}).get_text())
                    print('--' * 20)
            except AttributeError:
                    print('There is should be some text, but isn"t. My apologize!')
                    print('--'*20)

news_parsing()