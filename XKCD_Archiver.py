import requests
import wget
import dataset
import re
db = dataset.connect('sqlite:///C:\\Users\Tom\\PycharmProjects\\XKCD_Archiver\\XKCD_List.db')
db_name = 'XKCD'
table = db[db_name]


def current_comic_number():
    current_url = requests.get('http://xkcd.com/info.0.json')
    current_comic = current_url.json()
    current_number = current_comic['num']
    return current_number


def last_downloaded():
    result = db.query('SELECT comic_number FROM XKCD WHERE id IN (SELECT MAX(id) FROM XKCD)')
    for row in result:
        last_number = row['comic_number']
        if last_number is None:
            last_number = 0
        return last_number


def downloader(link):
    url = requests.get(link)
    if url.status_code == 404:
        print("404 LOL")
        table.insert(dict(comic_number='404', comic_title='404 Not Found', comic_url='404 Not Found'))
    else:
        comic = url.json()
        file_type = comic['img'][-4:]
        comic_title = re.sub('[^a-zA-Z0-9\n\.]', ' ', comic['title'])
        output = 'pics\\' + '#' + str(comic['num']) + ' ' + comic_title + file_type
        wget.download(comic['img'], output)
        table.insert(dict(comic_number=comic['num'], comic_title=comic['title'], comic_url=comic['img']))
        print('#' + str(comic['num']) + ' is done')


def main_loop():
    for count in range(last_downloaded(), current_comic_number()):
        comic_number = last_downloaded() + 1
        downloader('http://xkcd.com/' + str(comic_number) + '/info.0.json')

main_loop()
