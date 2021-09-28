# Parsing-napartner.ru
Parsing using the <b>requests</b> and <b>BeautifulSoup</b> library

You need to collect the following data:
  <ul><li>Startup name</li></ul>
  <ul><li>Link to the startup</li></ul>
  <ul><li>Information about the startup</li></ul>
  <ul><li>Startup image</li></ul>


<h1></h1>
<h1>How to use</h1>

1️⃣ Importing libraries

```python
import requests
from bs4 import BeautifulSoup
import csv
import os
```

`Requests makes a request to the server`

`BeautifulSoup allows you to transform a complex HTML document into a complex tree of various Python objects`

`A CSV file is a text file in which each line has several fields separated by commas, or other separators`

`The os module provides many functions for working with the operating system`



2️⃣ Declaring constants

```python
HOST = 'https://www.napartner.ru'
URL = 'https://www.napartner.ru/startups'
PAGE = '/page/'
FILE = 'start_up.csv'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    '(KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.2.381 Yowser/2.5 Safari/537.36',
}
```
3️⃣ Declaring the get_html function

```python
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r
```
The function will return the value 200 if the request was executed successfully


4️⃣In the get_content() function, we create a soup object and collect the necessary page elements

```python
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
```

5️⃣ We declare the main function parse(), in which we call all the functions

```python
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
```

6️⃣ The get_pages() function calculates the number of pages

```python
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='counter')
    if pagination:
        return int(pagination[-1].get_text())
    return 1
```

7️⃣ Using the save_file() function, we save the data in CSV format

```python
def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Ссылка', 'Информация', 'Изображение'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['info'], item['img']])
```

8️⃣ Calling the os.startfile(FILE) function with the FILE parameter

```python
os.startfile(FILE)
```

9️⃣ Calling the parse() function

```python
parse()
```





