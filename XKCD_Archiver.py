import requests
import re
from time import sleep
import os

pic_dir = r'C:\Users\Tom\Documents\Python_Projects\XKCD_Archiver\pics'
file_types = ('.png', '.jpg', '.gif')


def download_file(download_url, folder_structure, file_name):
    image_file = requests.get(download_url, stream=True)
    file_path = os.path.join(folder_structure, file_name)
    with open(file_path, 'wb') as f:
        f.write(image_file.content)


def current_comic_number():
    current_url = requests.get('http://xkcd.com/info.0.json')
    current_comic = current_url.json()
    current_number = current_comic['num']
    return current_number


def last_downloaded():
    pic_list = []
    for comics in os.scandir(pic_dir):
        if 'Thumbs.db' not in comics.name:
            pic_number = (comics.name[1:]).split(' ')[0]
            pic_list.append(int(pic_number))
    if len(pic_list) is 0:
        last_number = 0
    else:
        last_number = max(pic_list)
    return last_number


def downloader(download_comic_number):
    url = requests.get('http://xkcd.com/{}/info.0.json'.format(download_comic_number))
    if url.status_code == 404:
        print("404 LOL")
    else:
        comic = url.json()
        comic_url = comic['img']
        comic_number = str(comic['num'])
        file_type = os.path.splitext(comic['img'])[-1]
        comic_title = re.sub('[^a-zA-Z0-9\n\.]', ' ', comic['title'])
        if comic_url.endswith(file_types):
            pic_name = '#{} {}{}'.format(comic_number, comic_title, file_type)
            download_file(comic_url, pic_dir, pic_name)
            print('#{} is done'.format(comic_number))
        else:
            print('comic #{} doest not have a downloadable url'.format(comic_number))
            pic_name = '#{} {}.png'.format(comic_number, comic_title)
            download_file('http://i.imgur.com/removed.png', pic_dir, pic_name)


if __name__ == '__main__':
    for count in range(last_downloaded(), current_comic_number()):
        new_comic_number = str(last_downloaded() + 1)
        downloader(new_comic_number)
        sleep(1)
