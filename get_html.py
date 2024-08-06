import requests
import time
import logging


# Функция для получения HTML-кода страницы

def get_html(url, max_attempts=5, headers=None):
    attempt = 0
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36',
            'Accept': '*/*'
        }

    while attempt < max_attempts:
        try:
            response = requests.get(url, headers=headers)  # Используем переданные заголовки
            response.raise_for_status()  # Проверка на ошибки HTTP
            return response
        except requests.RequestException as e:
            logging.warning(f'Ошибка при загрузке {url}: {e}')
            attempt += 1
            time.sleep(10)  # Задержка перед повторной попыткой

    logging.error(f'Не удалось загрузить страницу {url} после {max_attempts} попыток.')
    return None
