import requests
from bs4 import BeautifulSoup

HOST = "https://minfin.com.ua/"
URL = 'https://minfin.com.ua/ua/currency/crypto/'
PAGENATION = '?page='
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_contentmain(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="sc-18qu8it-0 DHeKM")
    crypto = []

    for item in items:
        crypto.append(
            {
                'title': item.find('div', class_="sc-18qu8it-11 hZgTBs").get_text(),
                'letters': item.find('div', class_="sc-18qu8it-4 iuVTOJ").get_text(),
                'place': item.find('div', class_="sc-18qu8it-12 ichjdG").get_text(),
                'link': HOST + item.find('a', class_="sc-18qu8it-2 hmBaVo").get('href')
            }
        )
    return crypto

def get_contentprice(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_="sc-18qu8it-3 fygJIH")
    crypto = []
    for item in items:
        crypto.append(
            {
                'price': item.text
            }
        )
    return crypto

def get_contentcapital(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_="sc-18qu8it-0 sc-18qu8it-1 hAzOTj cDjrBt")
    crypto = []
    for item in items:
        crypto.append(
            {
                'capital': item.text
            }
        )
    return crypto

def get_contenthour(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_="sc-18qu8it-0 hAzOTj")
    crypto = []
    for item in items:
        if '%' in item.text:
            crypto.append(
                {
                    'hour': item.text
                }
            )
    return crypto

def content(html):
    main = get_contentmain(html.text)
    price = get_contentprice(html.text)
    capital = get_contentcapital(html.text)
    hour = get_contenthour(html.text)
    content = []
    content.append(main)
    content.append(price)
    content.append(capital)
    content.append(hour)
    return content

def pagenation(n):
    url = URL + PAGENATION + str(n)
    html = get_html(url)
    cont = content(html)
    return cont

def beutifullist(list):
    newlist = []
    for x in range(0, 50):
        newlist.append(
            {
                'title': list[0][x]['title'],
                'small_title': list[0][x]['letters'].replace(list[0][x]['place'], ''),
                'place': list[0][x]['place'],
                'link': list[0][x]['link'],
                'price' : list[1][x]['price'],
                'capital' : list[2][x]['capital'],
                'hour' : list[3][x]['hour']
            }
        )
    return newlist