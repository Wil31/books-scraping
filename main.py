import csv

import requests
from bs4 import BeautifulSoup

product_page_url = url = 'https://books.toscrape.com/catalogue/its-only-the-himalayas_981/'

response = requests.get(url)

if response.ok:
    soup = BeautifulSoup(response.text, 'lxml')
    tds = soup.findAll('td')
    universal_product_code = tds[0].text
    price_including_tax = tds[3].text
    price_excluding_tax = tds[2].text
    number_available = tds[-2].text
    title = soup.find("h1").text
    last_tag = soup.find('div', id="product_description")
    product_description = last_tag.find_next('p')

en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax",
           "price_excluding_tax", "number_available", "product_description", "category",
           "review_rating", "image_url"]

# with open('data.csv', 'w') as fichier_csv:
#     writer = csv.writer(fichier_csv, delimiter=',')
#     writer.writerow(en_tete)
#     for
