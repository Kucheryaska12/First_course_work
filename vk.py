import requests
import json
import logging
import configparser
from pprint import pprint

logging.basicConfig(level=logging.DEBUG, filename="log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

config = configparser.ConfigParser()
config.read('settings.ini')

class VK:
    def __init__(self, access_token, user_id, version='5.199'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}



    def albums_list(self): # метод создает список id альбомов пользователя, включая альбомы по умолчанию.
        url = 'https://api.vk.com/method/photos.getAlbums'
        params = self.params
        params.update({'owner_id': self.id})
        response = requests.get(url, params=params)
        albums_list = ['wall', 'profile', 'saved']
        for album_id in response.json()['response']['items']:
            albums_list.append(str(album_id['id']))
        logging.info(f'User {self.id} have albums: {', '.join(albums_list)}')
        return albums_list

    def _album_info(self, album_id): # метод вытаскивает массив информации о всех фотографиях, содержащихся в конкретном альбоме
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id, 'album_id': album_id, 'extended': 1}
        response = requests.get(url, params={**self.params,
        **params})
        logging.info(f'{self.id} users photo info from album {album_id} saved in Response')
        return response.json()
    
    def create_photo_size_max_album(self, album_id, cnt_photo=5): # метод создает список заданного количества словарей, содержащих информацию о наибольших по размеру фотографиях 
        photo_size_max_album = []
        photo_counter = 0
        likes_cnt_list = []
        for photo_size in self._album_info(album_id)['response']['items']:
            if photo_counter < cnt_photo:
                own_likes_cnt = photo_size['likes']['count']
                own_date_create = photo_size['date']
                own_photo_sizes = {}
                for own_photo_info in photo_size['sizes']:
                    sz = own_photo_info['height'] * own_photo_info['width']
                    url = own_photo_info['url']
                    type = own_photo_info['type']
                    own_photo_sizes[url] = [sz, type]
                size_max = 0
                url_max = 0
                type_max = 0
                for url_1 in own_photo_sizes:
                    if own_photo_sizes[url_1][0] > size_max:
                        url_max = url_1
                        type_max = own_photo_sizes[url_1][1]
                if own_likes_cnt in likes_cnt_list:
                    photo_name = f'{own_likes_cnt}_{own_date_create}'
                else:
                    photo_name = f'{own_likes_cnt}'
                    likes_cnt_list.append(own_likes_cnt)
                photo_info = {"file_name":photo_name, "size":type_max}
                photo_size_dict = {photo_name : [url_max, photo_info]}
                photo_size_max_album.append(photo_size_dict)
                photo_counter += 1
                
        logging.info(f'{cnt_photo} biggest photos added to photo_size_max_album')        
        return photo_size_max_album


class Ya:
    def __init__(self, access_token):
        self.token = access_token

    def create_ya_folder(self, album_name): # метод создает альбом на яндекс диске с заданным названием
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Authorization': f'OAuth {self.token}'}
        params = {'path': album_name}
        response = requests.put(url, params=params, headers=headers)
        logging.info(f'Folder {album_name} created in ya.disk')
        return response.json()
        
    def add_photo_to_folder(self, album_name, photo_url, photo_name): # метод сохраняет в имеющуюся папку на Яндекс.Диске фотографии по URL
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Authorization': f'OAuth {self.token}'}
        params = {'path': f'{album_name}/{photo_name}.jpg', 'url': photo_url}
        response = requests.post(url, params = params, headers=headers)
        logging.info(f'Photo {photo_name} added to folder {album_name}')
        return response.json()

access_token = config['Tokens']['vk_token'] # токен полученный из инструкции
ya_token = config['Tokens']['ya_token']
user_id = 54450950 # идентификатор пользователя vk


vk = VK(access_token, user_id)
ya = Ya(ya_token)


ya.create_ya_folder('VK_photos') # создаем папку на Яндекс.Диске
info_about_photos = [] # список с информацией о фотографиях в заданном формате
for photo in vk.create_photo_size_max_album('wall'): # сохраняем в папку на Яндекс.Диске фотографии из списка 
        photo_url = list(photo.values())[0][0]
        photo_name = list(photo.keys())[0]
        info_about_photos.append(list(photo.values())[0][1])
        ya.add_photo_to_folder('VK_photos', photo_url, photo_name)

with open('photos_info.json', 'w') as f: # создаем json-файл с информацией о фотографиях
        json.dump(info_about_photos, f, indent = 4)
        logging.info(f'photo info added to photos_info.json file')
