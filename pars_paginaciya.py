import csv
import os
import time
import json
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from parse_multiple_pages import parse_multiple_pages
from get_html import get_html

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Базовый URL страницы для парсинга
BASE_URL = 'https://www.che168.com/china/richan/tuda/a3_5'


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

            # Проверяем, что ссылка не содержит '/TopicApp/' и соответствует нужному формату
            if '/TopicApp/' not in absolute_link and 'che168.com/dealer/' in absolute_link:
                cars.append(absolute_link)  # Добавляем ссылку в список

    return cars  # Возвращаем список ссылок


# Функция для чтения существующих URL из CSV файла
def read_existing_urls(csv_file):
    existing_urls = set()
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_urls.add(row['url'])  # Предполагаем, что заголовок колонки 'url'
    except FileNotFoundError:
        logging.warning(f'Файл {csv_file} не найден, будет создан новый.')
    return existing_urls


# Запись в CSV
def write_to_csv(details, filename):
    # Проверяем, существует ли файл и не пустой ли он
    file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=details[0].keys())

        # Если файл не существует или он пустой, записываем заголовки
        if not file_exists:
            writer.writeheader()

        if details:  # Проверяем, что список не пустой
            for detail in details:
                writer.writerow(detail)
        else:
            logging.error('Список details пуст. Невозможно записать в CSV.')


# Основная функция парсинга
def parse():
    page_number = 1  # Начинаем с первой страницы
    all_car_links = []  # Список для хранения всех ссылок на автомобили

    # Сначала собираем все ссылки на автомобили
    while True:
        # Формируем URL для страницы
        page_url = (f'{BASE_URL}'
                    f'msdgscncgpi1ltocsp{page_number}exx0/')
        logging.info(f'Парсинг страницы {page_url}...')
        time.sleep(5)
        html = get_html(page_url)

        csv_file = 'd-max.csv'
        existing_urls = read_existing_urls(csv_file)

        if html.status_code == 200:
            cars = get_content(html.text)  # Получаем список ссылок

            if not cars:  # Если нет автомобилей на странице, выходим из цикла
                break
            # Фильтруем автомобили, оставляя только те, которые нет в existing_urls
            filtered_cars = [car for car in cars if car not in existing_urls]

            # Теперь добавляем отфильтрованные ссылки в общий список
            all_car_links.extend(filtered_cars)

            # Обновляем множество существующих URL
            existing_urls.update(filtered_cars)

            page_number += 1  # Переход к следующей странице
        else:
            logging.error('Ошибка при получении страницы или статус не 200')
            break

    # Теперь парсим каждую ссылку для получения деталей
    dict_file_path = 'replacement_dict.json'

    # Загружаем словарь из файла
    replacement_dict = load_replacement_dict(dict_file_path)
    details = parse_multiple_pages(all_car_links, replacement_dict)  # Получаем детали каждого автомобиля

    # Запись данных в CSV файл
    csv_file = 'd-max.csv'
    if details:  # Проверяем, что список не пустой
        write_to_csv(details, csv_file)
        print(f'Data has been written to {csv_file}')
    else:
        logging.warning('Список деталей пуст. Ничего не записано в CSV.')


"""
    for car in details:
        print(car)


    for car in all_car_links:
        details = parse_multiple_pages(car, replacement_dict)  # Получаем детали каждого автомобиля
        if details:
            car_data.append(details)  # Добавляем данные в список


    # Выводим собранные данные
    for car in car_data:
        print(car)
"""

parse()
