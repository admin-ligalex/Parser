import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = 'https://www.che168.com/china/changan/changancs75plus/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36',
    'Accept': '*/*'
}

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='carinfo')

    cars = []
    for item in items:
        link = item.get('href')
        if link:
            absolute_link = urljoin(BASE_URL, link.split('?')[0])
            cars.append(absolute_link)

    return cars  # Возвращаем список ссылок

def parse():
    page_number = 1  # Начинаем с первой страницы
    car_data = []

    while True:
        # Формируем URL для текущей страницы
        page_url = f'{BASE_URL}a3_5msdgscncgpi1ltocsp{page_number}exx0/'

        print(f'Парсинг страницы {page_url}...')
        time.sleep(1)
        html = get_html(page_url)

        if html.status_code == 200:
            cars = get_content(html.text)  # Получаем список ссылок

            if not cars:  # Если нет автомобилей на странице, выходим из цикла
                break

            car_data.extend(cars)  # Добавляем ссылки на автомобили в общий список
            page_number += 1  # Переход к следующей странице

        else:
            print('Error fetching page')
            break

    # Выводим собранные данные
    for car in car_data:
        print(car)

parse()
