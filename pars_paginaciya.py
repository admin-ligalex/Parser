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
BASE_URL = 'https://www.che168.com/china/wushiling/dmax/a3_5'
csv_file = 'CSV/cars_data1.csv'



def load_replacement_dict(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# Функция для извлечения ссылок на автомобили
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='carinfo')  # Находим все ссылки на автомобили

    cars_images = {}  # Словарь для хранения пар "ссылка на автомобиль - изображение"

    for item in items:
        link = item.get('href')
        if link:
            absolute_link = urljoin(BASE_URL, link.split('?')[0])  # Преобразуем относительную ссылку в абсолютную

            # Проверяем, что ссылка соответствует нужному формату
            if '/TopicApp/' not in absolute_link and 'che168.com/dealer/' in absolute_link:
                # Находим изображение внутри элемента
                img_tag = item.find('img', src=True)  # Находим тег img с атрибутом src
                img_src = img_tag['src'] if img_tag else None  # Получаем ссылку на изображение

                # Добавляем протокол, если нужно
                if img_src and img_src.startswith('//'):
                    img_src = 'https:' + img_src

                # Добавляем в словарь только если изображение найдено
                if img_src:
                    cars_images[absolute_link] = img_src  # Связываем ссылку на автомобиль с изображением

    return cars_images  # Возвращаем словарь


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
    all_car_links = {}  # Словарь для хранения всех ссылок на автомобили и их изображений

    # Сначала собираем все ссылки на автомобили
    while True:
        # Формируем URL для страницы
        page_url = (f'{BASE_URL}'
                    f'msdgscncgpi1ltocsp{page_number}exr3/')  # exr3 exx0
        logging.info(f'Парсинг страницы {page_url}...')
        time.sleep(5)
        html = get_html(page_url)

        existing_urls = read_existing_urls(csv_file)

        if html.status_code == 200:
            cars_images = get_content(html.text)  # Получаем словарь ссылок и изображений

            if not cars_images:  # Если нет автомобилей на странице, выходим из цикла
                break

            # Фильтруем автомобили, оставляя только те, которые нет в existing_urls
            filtered_cars = {link: img for link, img in cars_images.items() if link not in existing_urls}

            # Теперь добавляем отфильтрованные ссылки в общий словарь
            all_car_links.update(filtered_cars)

            # Обновляем множество существующих URL
            existing_urls.update(filtered_cars.keys())

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
