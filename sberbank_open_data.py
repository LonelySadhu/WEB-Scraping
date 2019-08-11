import pandas as pd
import matplotlib.pyplot as plt
from pylab import rcParams
from pprint import pprint


DATA = pd.read_csv('opendata.csv', encoding='cp1251')

#Выбираем категорию данных, по которой хотим получить информацию
NAMES = {
    1: 'Количество заявок на потребительские кредиты',
    2: 'Средняя сумма заявки на потребительский кредит',
    3: 'Количество заявок на ипотечные кредиты',
    4: 'Средняя сумма заявки на ипотечный кредит',
    5: 'Средняя зарплата',
    6: 'Средняя пенсия',
    7: 'Количество новых депозитов',
    8: 'Средняя сумма нового депозита',
    9: 'Средние расходы по картам',
    10: 'В среднем руб. на текущем счете на человека',
    11: 'В среднем депозитов в руб. на человека',
    12: 'Средний чек в формате Фастфуд',
    13: 'Средний чек в формате Ресторан',
    14: 'Средние траты в ресторане фастфуд',
    15: 'Средние траты в ресторане'
}

def input_params():

    pprint(NAMES)
    name = int(input('Введите номер категории выборки данных: '))
    year = str(input('Введите год за который хотите получить статистику (2013-2018): '))
    region = input('Введите регион: ')
    return NAMES[name], year, region


def data_show(params, df=DATA):

    print(params)
    name = params[0]
    year = params[1]
    region = params[2]
    values_array = df.loc[(df['date'].apply(lambda x: x[:4]) == year) & (df['name'] == name) & (df['region'] == region), 'value'].values
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    rcParams['figure.figsize'] = 12, 6
    title_dict = {'fontsize': 20, 'fontweight': 'bold', 'color': '#808080', 'family': 'Calibri'}
    label_dict = {'fontsize': '14', 'color': '#808080', 'family': 'Calibri'}
    plt.title(name, fontdict=title_dict)
    plt.ylabel('руб.', fontdict=label_dict)
    plt.xlabel(region, fontdict=label_dict)
    plt.plot(months, values_array)
    plt.show()



data_show(input_params())

