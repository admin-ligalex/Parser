import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Базовый URL страницы для парсинга
BASE_URL = 'https://www.che168.com/china/fengtian/rav4rongfang/'

# Заголовки для имитации браузера
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36',
    'Accept': '*/*'
}

# Функция для получения HTML-кода страницы
def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r

# Функция для извлечения ссылок на автомобили
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='carinfo')  # Находим все ссылки на автомобили

    cars = []
    for item in items:
        link = item.get('href')  # Получаем атрибут href
        if link:
            absolute_link = urljoin(BASE_URL, link.split('?')[0])  # Преобразуем относительную ссылку в абсолютную
            cars.append(absolute_link)  # Добавляем ссылку в список

    return cars  # Возвращаем список ссылок

# Функция для получения деталей автомобиля
def get_car_details(car_url):
    time.sleep(5)  # Задержка перед загрузкой страницы автомобиля
    html = get_html(car_url)
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')

        title = soup.find('h3').text.strip() if soup.find('h3') else 'Нет названия'  # Название автомобиля
        price_element = soup.find('span', class_='price')
        price = price_element.text.strip() if price_element else 'Цена не указана'  # Цена автомобиля

        return {
            'url': car_url,
            'title': title,
            'price': price,
        }
    else:
        print(f'Error fetching details for {car_url}')
        return None

# Основная функция парсинга
def parse():
    page_number = 1  # Начинаем с первой страницы
    all_car_links = []  # Список для хранения всех ссылок на автомобили

    # Сначала собираем все ссылки на автомобили
    while True:
        # Формируем URL для текa3_5msdgscncgpi1ltocsp1exr3
        page_url = f'{BASE_URL}a3_5msdgscncgpi1ltocsp{page_number}exr3/' #exx0/'
        print(f'Парсинг страницы {page_url}...')
        time.sleep(5)
        html = get_html(page_url)

        if html.status_code == 200:
            cars = get_content(html.text)  # Получаем список ссылок

            if not cars:  # Если нет автомобилей на странице, выходим из цикла
                break

            all_car_links.extend(cars)  # Добавляем собранные ссылки в общий список
            page_number += 1  # Переход к следующей странице
        else:
            print('Error fetching page')
            break

    # Теперь парсим каждую ссылку для получения деталей
    car_data = []  # Список для хранения данных об автомобилях
    for car in all_car_links:
        details = get_car_details(car)  # Получаем детали каждого автомобиля
        if details:
            car_data.append(details)  # Добавляем данные в список

    # Выводим собранные данные
    for car in car_data:
        print(car)

parse()