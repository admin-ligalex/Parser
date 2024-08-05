import time
import re

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL страницы для парсинга
URL = 'https://www.che168.com/china/wushiling/dmax/'

# Заголовки для имитации браузера
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36',
    'Accept': '*/*'
}

# Функция для получения HTML-кода страницы
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

# Функция для извлечения ссылок на автомобили
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='carinfo')  # Находим все ссылки на автомобили

    cars = []
    for item in items:
        link = item.get('href')  # Получаем атрибут href
        if link:
            absolute_link = urljoin(URL, link.split('?')[0])  # Преобразуем относительную ссылку в абсолютную
            cars.append(absolute_link)  # Добавляем ссылку в список

    return cars  # Возвращаем список ссылок


def get_car_details(car_url):
    time.sleep(5)
    # Получаем HTML-код страницы автомобиля
    html = get_html(car_url)
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')

        # извлечения информации
        title = soup.find('h3').text.strip() if soup.find('h3') else 'Нет названия'  # Название автомобиля
        price_element = soup.find('span', class_='price')
        price = price_element.text.strip() if price_element else 'Цена не указана'  # Цена автомобиля
      #  details = soup.find('div', class_='details').text.strip()  # Характеристики

        # Получение всех тегов h4
        h4_elements = soup.find_all('h4')

        # Помещение содержимого h4 в разные переменные

        if len(h4_elements) > 2:
            mileage = h4_elements[2].get_text(strip=True) or "Нет данных"
        else:
            mileage = "Нет данных"
        if mileage != "Нет данных":
            # Удаляем символы, которые не являются цифрами или точками
            numbers_only = re.sub(r'[^\d.]', '', mileage)

            if numbers_only:  # Проверяем, что строка не пустая
                # Преобразуем строку в число с плавающей запятой
                price_value = float(numbers_only)

                # Умножаем на 10 тысяч
                mileage = price_value * 10000  # Сохраняем результат в mileage

                # Форматируем результат обратно в строку с символом ¥ (если это нужно для вывода)
                mileage = f"{mileage:}"
            else:
                mileage = "Нет данных"  # Если numbers_only пусто, устанавливаем сообщение об ошибке
        else:
            mileage = "Нет данных"

        if len(h4_elements) > 3:
            registration_time = h4_elements[3].get_text(strip=True) or "Нет данных"
        else:
            registration_time = "Нет данных"

        if len(h4_elements) > 4:
            gear_and_displacement = h4_elements[4].get_text(strip=True) or "Нет данных"
        else:
            gear_and_displacement = "Нет данных"

        if len(h4_elements) > 4:
            location = h4_elements[5].get_text(strip=True) or "Нет данных"
        else:
            location = "Нет данных"


        return {
            'url': car_url,
            'title': title,
            'price': price,
            'mileage': mileage,
            'registration_time': registration_time,
            'gear_and_displacement': gear_and_displacement,
            'location': location,
          #  'details': details,
        }
    else:
        print(f'Error fetching details for {car_url}')
        return None

# Основная функция парсинга
def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = get_content(html.text)  # Получаем список ссылок
        car_data = []

        for car in cars:
            details = get_car_details(car)  # Получаем детали каждого автомобиля
            if details:
                car_data.append(details)  # Добавляем данные в список

            time.sleep(2)

        # Выводим собранные данные
        for car in car_data:
            print(car)
    else:
        print('Error')


parse()