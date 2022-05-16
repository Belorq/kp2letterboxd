import pandas as pd
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from math import ceil

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars") 
driver = webdriver.Chrome(executable_path="\\kp2letterboxed--\\chromedriver\\chromedriver.exe", options=options)


user_id = 'ENTER YOUR ID' 
data = []

#gets number of pages
def get_number(user_id):
    url = f'https://www.kinopoisk.ru/user/{user_id}/votes/list/ord/date/page/1/#list'
    driver.get(url=url)
    time.sleep(15)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    number = soup.find('div', class_='pagesFromTo').text.split()[-1]
    return ceil(float(number) / 50)

#scraping
def get_movies(user_id, data):
    for p in range(1, get_number(user_id) + 1):
        url = f'https://www.kinopoisk.ru/user/{user_id}/votes/list/ord/date/page/{p}/#list'
        driver.get(url=url)
        time.sleep(15)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        films = soup.find('div', class_='profileFilmsList').find_all('div', class_='item')
        for film in films:
            if film.find('div', class_='info').find('div', class_='nameEng').text.replace(u'\xa0',' ') == ' ':
                nameEng = film.find('div', class_='info').find('div', class_='nameRus').find('a').text[:-7]
            else:
                nameEng = film.find('div', class_='info').find('div', class_='nameEng').text  
            year = film.find('div', class_='info').find('div', class_='nameRus').find('a').text[-5:-1]
            rating = film.find('div', class_='vote').text
            data.append( [nameEng, year, rating] )

#making csv
def csv(data):
    df = pd.DataFrame(data, columns = ['Name', 'Year', 'Rating10'])
    df.set_index('Name', inplace=True)
    df.to_csv('C:\\kp2letterboxed--\\chromedriver\\kp_data.csv', encoding='utf8')


def main(user_id, data):
    get_number(user_id)

    get_movies(user_id, data)

    csv(data)

    driver.quit()

if __name__ == '__main__':
    main(user_id, data)