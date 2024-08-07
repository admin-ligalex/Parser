import time
import json
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium_details import selenium_details
from get_html import get_html

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Базовый URL страницы для парсинга
BASE_URL = 'https://www.che168.com/china/richan/richangtr/a0_0'


def load_replacement_dict(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


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


# Основная функция парсинга
def parse():
    page_number = 1  # Начинаем с первой страницы
    all_car_links = []  # Список для хранения всех ссылок на автомобили

    # Сначала собираем все ссылки на автомобили
    while True:
        # Формируем URL для текa3_5msdgscncgpi1ltocsp1exr3
        page_url = (f'{BASE_URL}'
                    f'msdgscncgpi1ltocsp{page_number}exx0/')  # exr3/'  # exx0/'
        logging.info(f'Парсинг страницы {page_url}...')
        #time.sleep(10)
        html = get_html(page_url)

        if html.status_code == 200:
            cars = get_content(html.text)  # Получаем список ссылок

            if not cars:  # Если нет автомобилей на странице, выходим из цикла
                break

            all_car_links.extend(cars)  # Добавляем собранные ссылки в общий список
            page_number += 1  # Переход к следующей странице
        else:
            logging.error('Ошибка при получении страницы или статус не 200')
            break

    # Теперь парсим каждую ссылку для получения деталей
    car_data = []  # Список для хранения данных об автомобилях
    # Путь к файлу со словарем
    dict_file_path = 'replacement_dict.json'

    # Загружаем словарь из файла
    replacement_dict = load_replacement_dict(dict_file_path)

    for car in all_car_links:
        details = selenium_details(car, replacement_dict)  # Получаем детали каждого автомобиля
        if details:
            car_data.append(details)  # Добавляем данные в список

    # Выводим собранные данные
    for car in car_data:
        print(car)


parse()
