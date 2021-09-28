import requests
from bs4 import BeautifulSoup
import csv
import os

HOST = 'https://www.napartner.ru'
URL = 'https://www.napartner.ru/startups'
PAGE = '/page/'
FILE = 'start_up.csv'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    '(KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.2.381 Yowser/2.5 Safari/537.36',


}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='counter')
    if pagination:
        return int(pagination[-1].get_text())
    return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='main_startup_view')

    cards = []
    for item in items:
        cards.append({
            'title': item.find('div', class_='name').get_text(),
            'link': HOST + item.find('a').get('href'),
            'info': item.find('div', class_='hars').get_text().replace('\n', ''),
            'img': HOST + item.find('div', class_='img').find('img').get('src')
        })

    return cards


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Ссылка', 'Информация', 'Изображение'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['info'], item['img']])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        pages_count = get_pages_count(html.text)
        for page in range(0, pages_count + 14):
            print(f'Parsin the page nummber {page + 1} of {pages_count + 15}')
            html = get_html(URL + PAGE + str(page))
            cards.extend(get_content(html.text))
        save_file(cards, FILE)
        print(f'Получено {len(cards)} стартапов')
        os.startfile(FILE)
    else:
        print('Error')
    return html


parse()

#github: https://github.com/quro4ka
