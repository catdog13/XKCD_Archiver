import requests
import wget
import re
from time import sleep
import os
pic_dir = r'C:\Users\Tom\Documents\Python_Projects\XKCD_Archiver\pics'


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


def downloader(link):
    url = requests.get(link)
    if url.status_code == 404:
        print("404 LOL")
    else:
        comic = url.json()
        comic_url = comic['img']
        file_type = comic['img'][-4:]
        comic_title = re.sub('[^a-zA-Z0-9\n\.]', ' ', comic['title'])
        output = '{}\\#{} {}'.format(pic_dir, str(comic['num']), comic_title + file_type)
        wget.download(comic_url, output)
        print('#' + str(comic['num']) + ' is done')


if __name__ == '__main__':
    for count in range(last_downloaded(), current_comic_number()):
        comic_number = last_downloaded() + 1
        downloader('http://xkcd.com/' + str(comic_number) + '/info.0.json')
        sleep(1)
