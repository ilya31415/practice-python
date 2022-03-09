import requests
from pprint import pprint


def test_request():
    url = 'https://superheroapi.com/api/2619421814940190/search/Thanos'
    response = requests.get(url=url)
    if response.status_code == 200:
        pprint(response.json())
    else:
        raise Exception('response.status_code????')


super_hero = ['Hulk', 'Captain America', 'Thanos', 'Superman']


def search_intelligence(name):
    name_intelligence = {}
    i = 0
    for name in super_hero:
        url = f'https://superheroapi.com/api/2619421814940190/search/{name}'
        response = requests.get(url)
        i += 1
        print(f'Идет загрузка информации по {i} герою...')
        name_intelligence[name] = int(response.json()['results'][0]['powerstats']['intelligence'])
    return f'Самый умный {max(name_intelligence, key=name_intelligence.get)}' \
           f' c показателем интеллекта {max(name_intelligence.values())}\n {name_intelligence} '


print(search_intelligence(super_hero))
