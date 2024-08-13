import logging
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor


def parse_price(price_text):
    numbers_only = re.sub(r'[^0-9.]', '', price_text)
    if numbers_only and numbers_only != '.':
        return f"{float(numbers_only) * 10000:.0f}"
    else:
        return 'нет данных'


class CarParser:
    def __init__(self):
        self.driver = None
        self.service = None
        self.options = None
        self.max_attempts = None
        self.chrome_driver_path = ('C:/Users/iuser/AppData/Local/Microsoft/WinGet/Packages/Chromium'
                                   '.ChromeDriver_Microsoft.Winget.Source_8wekyb3d8bbwe/chromedriver-win64'
                                   '/chromedriver.exe')

    def init(self, chrome_driver_path, max_attempts=3):
        self.chrome_driver_path = chrome_driver_path
        self.max_attempts = max_attempts
        self.options = Options()
        self.options.page_load_strategy = 'eager'
        self.service = Service(self.chrome_driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def parse_car_details(self, car_url, image_url, replacement_dict):
        attempt = 0
        while attempt < self.max_attempts:
            try:
                self.driver.get(car_url)
                logging.info(f'Парсинг страницы {car_url}...')

                title_element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'h3'))
                )
                price_element = self.driver.find_element(By.CSS_SELECTOR, 'span.price')
                engine_info = self.get_engine_info()

                mileage, year, month = self.get_mileage_and_registration_time()

                gear_and_displacement = self.get_gear_and_displacement()
                location = self.get_location(replacement_dict)

                if title_element and price_element:
                    title = title_element.text.strip()
                    price = parse_price(price_element.text.strip())

                    return {
                        'url': car_url,
                        'image_url': image_url,
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
                logging.error(f'Ошибка загрузки страницы {car_url}, попытка {attempt + 1} из {self.max_attempts}: {e}')
            attempt += 1

        logging.error(f'Не удалось загрузить страницу {car_url} после {self.max_attempts} попыток.')
        self.driver.quit()
        return None

    def get_engine_info(self):
        engine_info_elements = self.driver.find_elements(By.CSS_SELECTOR, 'ul.basic-item-ul li')
        for element in engine_info_elements:
            if '发  动  机' in element.text:
                return element.text.split('发')[1].strip()
        return None

    def get_mileage_and_registration_time(self):
        h4_elements = self.driver.find_elements(By.TAG_NAME, 'h4')
        mileage = h4_elements[2].text.strip() if len(h4_elements) > 2 else "Нет данных"
        registration_time = h4_elements[3].text.strip() if len(h4_elements) > 3 else "Нет данных"

        if mileage != "Нет данных":
            numbers_only = re.sub(r'[^0-9.]', '', mileage)
            if numbers_only and numbers_only != '.':
                mileage = float(numbers_only) * 10000
                mileage = f"{mileage:.0f}"
            else:
                mileage = "Нет данных"

        match = re.match(r'(\\d{4})年(\\d{2})月', registration_time)
        if match:
            year = match.group(1)
            month = match.group(2)
        else:
            year = "Нет данных"
            month = "Нет данных"

        return mileage, year, month

    def get_gear_and_displacement(self):
        h4_elements = self.driver.find_elements(By.TAG_NAME, 'h4')
        return h4_elements[4].text.strip() if len(h4_elements) > 4 else "Нет данных"

    def get_location(self, replacement_dict):
        h4_elements = self.driver.find_elements(By.TAG_NAME, 'h4')
        location = h4_elements[5].text.strip() if len(h4_elements) > 5 else "Нет данных"
        return replacement_dict.get(location, location)

    def parse_multiple_pages(self, car_details, replacement_dict):
        results = []

        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = {executor.submit(self.parse_car_details, url, car_details[url], replacement_dict): url for url in
                       car_details.keys()}

            for future in futures:
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as e:
                    logging.error(f'Ошибка при парсинге страницы: {futures[future]} - {e}')

        return results
