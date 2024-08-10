import logging
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor


def selenium_details(car_url, replacement_dict, max_attempts=3):
    #  extension_path = 'C:/Users/iuser/Documents/BrowsecVPN/'  # или путь к
    # распакованной папке
    options = Options()
    #  options.add_argument("--auto-open-devtools-for-tabs")  # Открывает инструменты разработчика при запуске
    #  options.add_extension(extension_path)
    options.page_load_strategy = 'eager'  # 'none'
    service = Service('C:/Users/iuser/AppData/Local/Microsoft/WinGet/Packages/Chromium.ChromeDriver_Microsoft.Winget'
                      '.Source_8wekyb3d8bbwe/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

    attempt = 0
    while attempt < max_attempts:
        try:
            driver.get(car_url)
            logging.info(f'Парсинг страницы {car_url}...')

            title_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, 'h3'))
            )
            price_element = driver.find_element(By.CSS_SELECTOR, 'span.price')
            engine_info = None

            engine_info_elements = driver.find_elements(By.CSS_SELECTOR, 'ul.basic-item-ul li')
            for element in engine_info_elements:
                if '发  动  机' in element.text:
                    engine_info = element.text.split('发')[1].strip()
                    break

            h4_elements = driver.find_elements(By.TAG_NAME, 'h4')
            mileage = h4_elements[2].text.strip() if len(h4_elements) > 2 else "Нет данных"

            if mileage != "Нет данных":
                # Удаляем все символы, кроме цифр и точки
                numbers_only = re.sub(r'[^0-9.]', '', mileage)

                # Проверяем, что в строке есть хотя бы одно число
                if numbers_only and numbers_only != '.':
                    mileage = float(numbers_only) * 10000
                    mileage = f"{mileage:.0f}"
                else:
                    mileage = "Нет данных"  # Или любое другое значение по умолчанию

            registration_time = h4_elements[3].text.strip() if len(h4_elements) > 3 else "Нет данных"
            match = re.match(r'(\d{4})年(\d{2})月', registration_time)
            if match:
                year = match.group(1)  # Год
                month = match.group(2)  # Месяц
            else:
                year = "Нет данных"
                month = "Нет данных"

            gear_and_displacement = h4_elements[4].text.strip() if len(h4_elements) > 4 else "Нет данных"
            location = h4_elements[5].text.strip() if len(h4_elements) > 5 else "Нет данных"
            location = replacement_dict.get(location, location)

            if title_element and price_element:
                title = title_element.text.strip()
                price = price_element.text.strip()
                numbers_only = re.sub(r'[^0-9.]', '', price)
                if numbers_only and numbers_only != '.':
                    price = float(numbers_only) * 10000
                    price = f"{price:.0f}"
                else:
                    price = 'нет данных'

                return {
                    'url': car_url,
                    'title': title,
                    'price': price,
                    'mileage': mileage,
                    'year': year,
                    'month': month,
                    'gear_and_displacement': gear_and_displacement,
                    'engine_info': engine_info,
                    'location': location,
                }
            else:
                logging.error(f'Не удалось найти необходимые элементы на странице {car_url}.')
                break
        except Exception as e:
            logging.error(f'Ошибка загрузки страницы {car_url}, попытка {attempt + 1} из {max_attempts}: {e}')
        attempt += 1

    logging.error(f'Не удалось загрузить страницу {car_url} после {max_attempts} попыток.')
    driver.quit()
    return None


def parse_multiple_pages(car_urls, replacement_dict):
    results = []

    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = {executor.submit(selenium_details, url, replacement_dict): url for url in car_urls}

        for future in futures:
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as e:
                logging.error(f'Ошибка при парсинге страницы: {futures[future]} - {e}')

    return results
