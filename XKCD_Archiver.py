import requests
import wget
import re
from time import sleep
import os
pic_dir = r'C:\Users\Tom\Documents\Python_Projects\XKCD_Archiver\pics'
file_types = ('.png', '.jpg', '.gif')


def current_comic_number():
    current_url = requests.get('http://xkcd.com/info.0.json')
    current_comic = current_url.json()
    current_number = current_comic['num']
    return current_number


def last_downloaded():
    pic_list = []
    for comics in os.scandir(pic_dir):
        pic_list.append(comics.name)
    last_number = len(pic_list)
    return last_number


def downloader(download_comic_number):
    url = requests.get('http://xkcd.com/{}/info.0.json'.format(download_comic_number))
    if url.status_code == 404:
        print("404 LOL")
    else:
        comic = url.json()
        comic_url = comic['img']
        comic_number = str(comic['num'])
        file_type = comic['img'][-4:]
        comic_title = re.sub('[^a-zA-Z0-9\n\.]', ' ', comic['title'])
        if comic_url.endswith(file_types):
            output = '{}\\#{} {}{}'.format(pic_dir, comic_number, comic_title, file_type)
            wget.download(comic_url, output)
            print('#{} is done'.format(comic_number))
        else:
            print('comic #{} doest not have a downloadable url'.format(comic_number))
            output = '{}\\#{} {}.png'.format(pic_dir, comic_number, comic_title)
            wget.download('http://i.imgur.com/removed.png', output)


if __name__ == '__main__':
    for count in range(last_downloaded(), current_comic_number()):
        new_comic_number = str(last_downloaded() + 1)
        downloader(new_comic_number)
        sleep(1)
