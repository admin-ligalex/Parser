import requests


def get_html_with_proxy(url, proxy):
    # Настройка прокси
    proxies = {
        "https": proxy,
    }

    try:
        # Выполнение GET-запроса
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении страницы: {e}")
        return None
