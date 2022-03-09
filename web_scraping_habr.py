import requests
import bs4
import re

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,'
              'application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '_ym_d=1639583840; _ym_uid=1639583840352909774;'
              ' hl=ru; fl=ru; visited_articles=349860:545150:321510:227377; _ym_isad=2; habr_web_home=ARTICLES_LIST_ALL',
    'Host': 'habr.com',
    'If-None-Match': 'W/"36ed0-kq+5ZtIHgEv/3J/rhZ/LVpftFRs"',
    'Referer': 'https://github.com/netology-code/py-homeworks-advanced/tree/master/6.Web-scrapping',
    'sec-ch-ua': '"Chromium";v="96", "Opera";v="82", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.58'

}


def text_data(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    text2 = response.text
    soup2 = bs4.BeautifulSoup(text2, features='html.parser')
    div_article = soup2.find_all('div', class_="tm-article-body")
    text_data = div_article[0].find_all('p')
    text_data = [data.text for data in text_data]
    return text_data


list_hups = {'Дизайн', 'Фото', 'Web', 'Python'}

for i in range(1, 5):
    print(f'Страница {i}')
    response = requests.get(f'https://habr.com/ru/all/page{i}/', headers=HEADERS)
    response.raise_for_status()
    text = response.text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    article = soup.find_all('article')

    for articl in article:
        time = articl.find_all('span', class_="tm-article-snippet__datetime-published")
        time = [time_data.find('time').text for time_data in time]
        hups = articl.find_all('a', class_="tm-article-snippet__hubs-item-link")
        hups = [hup.find('span').text for hup in hups]
        title = articl.find('h2')
        if list_hups & set(hups):
            link = title.find('a')['href']
            href_link = 'https://habr.com' + link
            join_str = '.'.join(text_data(href_link))
            split_s = re.split('\.', join_str)
            print(title.text)
            print(hups)
            print(time)
            print(href_link)
            print()
            print(f'Текст статьи: {join_str}')
            print()
            for element in list_hups:
                quote = [k for k in split_s if element in k]
                if len(quote) > 0:
                    print(f'Предложения где есть слово:"{element}"')
                    print('\n'.join(quote))

            print()
            print('----------')
            print('----------')
            print('----------')
