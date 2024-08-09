import re
import logging
import time
from bs4 import BeautifulSoup
from get_html import get_html


# Функция для получения деталей автомобиля
def get_car_details(car_url, replacement_dict, max_attempts=3):
    attempt = 0
    while attempt < max_attempts:
        time.sleep(5)  # Задержка перед загрузкой страницы автомобиля
        html = get_html(car_url)

        if html:  # and html.status_code == 200:
            soup = BeautifulSoup(html.text, 'html.parser')

            # Проверка наличия необходимых элементов на странице
            title_element = soup.find('h3')
            price_element = soup.find('span', class_='price')
            if price_element:
                number_only = re.sub(r'[^\d.]', '', price_element)
                if number_only:
                    price_value = float(number_only)
                    price_element = price_value * 10000
                    price_element = f"{price_element:.0f}"

            # Инициализируем переменную для хранения информации о двигателе
            engine_info = None

            # Находим элемент, используя CSS-селектор
            engine_info_element = soup.select_one(
                'ul.basic-item-ul li:has(span.item-name:-soup-contains("发  动  机"))')

            if engine_info_element:
                engine_info = engine_info_element.get_text(strip=True).split('发')[1].strip()

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

                    # Форматируем результат обратно в строку
                    mileage = f"{mileage:.0f}"
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

            # Замена значения location на значение из словаря, если найдено
            location = replacement_dict.get(location, location)

            if title_element and price_element:
                title = title_element.text.strip()
                price = price_element  #.text.strip()

                return {
                    'url': car_url,
                    'title': title,
                    'price': price,
                    'mileage': mileage,
                    'registration_time': registration_time,
                    'gear_and_displacement': gear_and_displacement,
                    'engine_info': engine_info,
                    'location': location,
                }
            else:
                logging.error(f'Не удалось найти необходимые элементы на странице {car_url}.')
                break  # Выход из цикла, если элементы не найдены
        else:
            logging.error(f'Ошибка загрузки страницы {car_url}, попытка {attempt + 1} из {max_attempts}')

        attempt += 1
        time.sleep(30)  # Задержка перед повторной попыткой

    logging.error(f'Не удалось загрузить страницу {car_url} после {max_attempts} попыток.')
    return None
