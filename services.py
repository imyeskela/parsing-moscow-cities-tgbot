from bs4 import BeautifulSoup
import pyrebase
from settings import config
import requests
firebase = pyrebase.initialize_app(config)
db = firebase.database()


def parsing_data():
    website = 'https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D1%81%D0%BA%D0%B8%D0%B5_%D0%BD%D0%B0%D1%81%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D0%B5_%D0%BF%D1%83%D0%BD%D0%BA%D1%82%D1%8B_%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B9_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D0%B8'
    result = requests.get(website)
    content = result.text
    soup = BeautifulSoup(content, 'lxml')
    tables = soup.select('#mw-content-text > div > table:nth-child(8) > tbody > tr')
    tables.pop(0)
    c = 0
    for table in tables:
        columns = table.select('td')
        c += 1
        name_city = columns[1].text
        population = columns[4]['data-sort-value']
        link_to_wiki = 'https://ru.wikipedia.org' + columns[1].find('a', href=True)['href']
        data = {
            'name': name_city,
            'population': population,
            'link': link_to_wiki
        }
        db.child('cities').child(name_city).set(data)


def search_city(name):
    cities = db.child('cities').get()
    for city in cities:
        if name.lower() == (city.key()).lower():
            get_city = db.child('cities').child(name).get()
            return get_city


def cities(name):
    cities = db.child('cities').get()
    city_list = []
    for city in cities:
        if name.lower() in (city.key()).lower():
            city_list.append(city.key())
    return city_list