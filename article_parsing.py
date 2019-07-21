import re
import collections
import requests

def return_wiki_html(topic):
    """returns wiki html-page in according with topic"""
    wiki_request = requests.get(f'https://ru.wikipedia.org/wiki/{topic.capitalize()}')
    return wiki_request.text

def link_parse(topic):
    """returns second link on the page"""
    wiki_html = return_wiki_html(topic)
    match = re.findall(r'href=[\'"]?(http[s]?[^\'" >]+)', wiki_html)
    print(f'В статье обнаружено {len(match)} текстовых ссылок')
    print(f'Проходим по ссылке {match[1]}...')  #Потому что первая ссылка ведет на эту же страницу
    return match[1]

def return_words(topic):
    """counts most common words on the page and print it"""
    some_html = requests.get(link_parse(topic)).text
    words = re.findall(r'[а-яА-Я]{4,}', some_html)
    words_counter = collections.Counter()
    for word in words:
        words_counter[word] += 1
    for word in words_counter.most_common(10):
        print(f'Слово {word[0]} встречается {word[1]} раз')

return_words("отпуск")

