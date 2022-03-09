from pprint import pprint
from datetime import datetime
import requests
from tqdm import tqdm


# Приложение скачивает фотографии пользователя Вк и загружает на яндекс диск.


class YaUploader:
    def __init__(self, token_Y: str, TOKEN_VK: str):
        self.token_Y = token_Y
        self.token_V = TOKEN_VK

    def vk_photo_get(self, id):
        return {'owner_id': id,
                'access_token': self.token_V,
                'v': '5.131',
                'album_id': 'wall',
                'count': '200',
                'extended': '1',
                }

    def get_uploead_link(self, disck_file: str):
        up_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.headers()
        params = {"path": disck_file, "overwrite": "false"}
        resource = requests.get(up_url, headers=headers, params=params)
        return resource.json()

    def mkdir_idname(self, id_vk):
        up_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.headers()
        path = self.id_vk_name(id_vk)
        params = {"path": path}
        resource = requests.put(up_url, headers=headers, params=params)
        return path

    def vk_download(self, id_vk):
        k = []
        global content
        url_vk = 'https://api.vk.com/method/photos.get'
        res = requests.get(url_vk, params=self.vk_photo_get(id_vk))
        items = res.json()['response']['items']
        for i in tqdm(items):
            dict_ = {}
            h = i['sizes']
            for a in h:
                way = a['type'][-1]
                if a['type'] == way:
                    url_photo = a['url']
                    likes = i['likes']['count']
                    content = requests.get(url_photo)
            k.append(1)
            dict_[content.content] = likes
            self.upload(dict_, id_vk)

        return pprint(f'Загрузил {len(k)} изображения')

    def id_vk_name(self, id_vk):
        url_vk = 'https://api.vk.com/method/users.get'
        params = {'access_token': self.token_V,
                  'user_ids': id_vk,
                  'v': '5.131'}
        res = requests.get(url_vk, params=params)
        for name in res.json()['response']:
            vk_name = "% s % s" % (name['first_name'], name['last_name'])
        return vk_name

    def upload(self, dict_down, id):
        date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")

        for i, x in dict_down.items():
            path = f'/{self.mkdir_idname(id)}/{str(x)} лайков. {date}'

            href = self.get_uploead_link(path).get("href", "")
            resource = requests.put(href, data=i)
            resource.raise_for_status()
            if resource.status_code == 201:
                print(f'Загрузил фото с {x} лайками \n')
            else:
                print(f'не удалось загрузить {x}')
            return

    def headers(self):
        return {'Content-Tape': 'application/json',
                'Authorization': 'OAuth {}'.format(self.token_Y)
                }

    def fails_list(self):
        fails_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.headers()
        resource = requests.get(fails_url, headers=headers)
        return resource.json()


if __name__ == '__main__':
    TOKEN_VK: str = ''
    TOKEN_YD = ''
    owner_id = ''

    photo_yandex = YaUploader(TOKEN_YD, TOKEN_VK)
    photo_yandex.vk_download(owner_id)
