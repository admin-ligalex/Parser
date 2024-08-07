from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import time
import re
import logging


def selenium_details(car_url, replacement_dict, max_attempts=3):
    # Настройка драйвера Chrome
    service = Service('C:/Users/iuser/AppData/Local/Microsoft/WinGet/Packages/Chromium.ChromeDriver_Microsoft.Winget'
                      '.Source_8wekyb3d8bbwe/chromedriver-win64/chromedriver.exe')  # Укажите путь к ChromeDriver
    driver = webdriver.Chrome(service=service)

    attempt = 0
    while attempt < max_attempts:
        try:
            driver.get(car_url)
            #time.sleep(10)  # Задержка перед загрузкой страницы автомобиля

            # Явное ожидание для необходимых элементов
            title_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'h3'))
            )
            price_element = driver.find_element(By.CSS_SELECTOR, 'span.price')

            # Инициализируем переменную для хранения информации о двигателе
            engine_info = None

            # Находим все элементы списка
            engine_info_elements = driver.find_elements(By.CSS_SELECTOR, 'ul.basic-item-ul li')
            for element in engine_info_elements:
                if '发  动  机' in element.text:
                    engine_info = element.text.split('发')[1].strip()
                    break

            # Получение всех тегов h4
            h4_elements = driver.find_elements(By.TAG_NAME, 'h4')

            # Помещение содержимого h4 в разные переменные
            mileage = h4_elements[2].text.strip() if len(h4_elements) > 2 else "Нет данных"
            if mileage != "Нет данных":
                # Удаляем символы, которые не являются цифрами или точками
                numbers_only = re.sub(r'[^\d.]', '', mileage)
                if numbers_only:  # Проверяем, что строка не пустая
                    mileage = float(numbers_only) * 10000  # Умножаем на 10 тысяч
                    mileage = f"{mileage:.0f}"  # Форматируем результат обратно в строку

            registration_time = h4_elements[3].text.strip() if len(h4_elements) > 3 else "Нет данных"
            gear_and_displacement = h4_elements[4].text.strip() if len(h4_elements) > 4 else "Нет данных"
            location = h4_elements[5].text.strip() if len(h4_elements) > 5 else "Нет данных"

            # Замена значения location на значение из словаря, если найдено
            location = replacement_dict.get(location, location)

            if title_element and price_element:
                title = title_element.text.strip()
                price = price_element.text.strip()

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

        except Exception as e:
            logging.error(f'Ошибка загрузки страницы {car_url}, попытка {attempt + 1} из {max_attempts}: {e}')

        attempt += 1
        #time.sleep(30)  # Задержка перед повторной попыткой

    logging.error(f'Не удалось загрузить страницу {car_url} после {max_attempts} попыток.')
    driver.quit()  # Закрываем драйвер перед выходом
    return None
