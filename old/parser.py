import requests
from bs4 import BeautifulSoup

URl = 'https://www.che168.com/china/wushiling/dmax/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36', 'accept': '*/*'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='carinfo')

    cars = []
    for item in items:
        link_el = item.find('a', class_='carinfo')
        if link_el is not None:
            link = link_el.get('href')
        else:
            link = None  
        cars.append({
            #'title': item.find('h4', class_='card-name').get_text(strip=True),
            'link': link,
        })
    print(cars)

def parse():
    html = get_html(URl)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')


parse()
