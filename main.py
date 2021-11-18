import requests
from bs4 import BeautifulSoup
import csv
import re
import os

SITE_URL = 'https://books.toscrape.com/'

CWD = os.getcwd()


# Extract a list of data from a specific book url input
def details_extractor(url):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')

        table = soup.findAll('td')
        universal_product_code = table[0].text

        price_including_tax = table[3].text
        price_including_tax = re.findall(r"[-+]?\d*\.\d+|\d+", price_including_tax)  # regular
        # expression operation to return all non-overlapping matches from the pattern
        # "[-+]?\d*\.\d+|\d+"
        price_including_tax = ''.join(map(str, price_including_tax))  # map() to convert each item
        # in the list to a string, and then join them

        price_excluding_tax = table[2].text
        price_excluding_tax = re.findall(r"[-+]?\d*\.\d+|\d+", price_excluding_tax)
        price_excluding_tax = ''.join(map(str, price_excluding_tax))

        stock_txt = table[-2].text
        number_available = ''.join(filter(str.isdigit, stock_txt))  # filter out only one number
        # from the string (only works for one number and int)

        title = soup.find("h1").text

        product_description = soup.find('div', id="product_description")
        if not product_description:
            product_description = "No description"
        else:
            product_description = product_description.find_next('p').text

        category = soup.find("ul", "breadcrumb").find_next("a").find_next("a").find_next("a").text

        stars = soup.find("div", class_="col-sm-6 product_main") \
            .find("p", class_="star-rating")['class']
        match stars[1].lower():
            case 'one':
                review_rating = '1'
            case 'two':
                review_rating = '2'
            case 'three':
                review_rating = '3'
            case 'four':
                review_rating = '4'
            case 'five':
                review_rating = '5'
            case _:
                review_rating = 'NA'

        img_url_raw = soup.find("div", class_="item active").find('img')['src']
        image_url = SITE_URL + img_url_raw.strip("./")

        download_img(image_url, title)
        #  Create a list with the data extracted from product page
        book_extract = [url, universal_product_code, title, price_including_tax,
                        price_excluding_tax, number_available, product_description, category,
                        review_rating, image_url]
        return book_extract
    else:
        return print("url_error")


# Create file 'filename'.csv in data folder and input the header
def create_csv(filename, header):
    filepath = os.path.join(CWD + '/data', filename)
    if not os.path.exists(CWD + '/data'):
        os.makedirs(CWD + '/data')
    with open(filepath + '.csv', 'w', encoding="utf-8") as file_csv:
        writer = csv.writer(file_csv, delimiter=',')  # Create writer object with this file
        writer.writerow(header)  # Write the header on first row


# Append a new row in '/data/filename'.csv file
def append_csv(filename, row):
    with open('./data/' + filename + '.csv', 'a', encoding="utf-8") as file_csv:
        for book_url in row:
            writer = csv.writer(file_csv, delimiter=',')
            writer.writerow(details_extractor(book_url))  # Append with the new row


# Extract all product links from a category input
def product_links_extractor(url):
    links = []
    cat_url = url.rstrip('index.html')
    while True:
        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')
            articles = soup.findAll('article', class_='product_pod')
            for article in articles:
                link = article.find('a')['href']
                link = link.strip("./")
                links.append(SITE_URL + 'catalogue/' + link)
            next_page = soup.find('li', class_='next')
            if not next_page:
                break
            next_url = soup.find("li", class_='next').find('a')['href']
            url = cat_url + next_url
        else:
            return print("url_error")
    return links


# Extract all book categories from 'https://books.toscrape.com/
def all_cats_extractor(url):
    cats_urls = []
    cats_names = []
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        cats = soup.find('ul', class_='nav nav-list').find('ul').findAll('a')
        for cat in cats:
            link = cat['href']
            cats_urls.append(SITE_URL + link)
            cat_name = cat.text.strip()
            cats_names.append(cat_name)
    else:
        return print("url error")
    return cats_urls, cats_names


def download_img(url, filename):
    invalid = '<>:"/\|?*'
    for char in invalid:
        filename = filename.replace(char, '')
    filename = filename.replace(' ', '_')
    r = requests.get(url, allow_redirects=True)
    if not os.path.exists(CWD + './data/images'):
        os.makedirs(CWD + './data/images')
    open('./data/images/' + filename + '.jpg', 'wb').write(r.content)


def main():
    # Header list for the csv file
    header_list = ["product_page_url", "universal_product_code", "title", "price_including_tax",
                   "price_excluding_tax", "number_available", "product_description", "category",
                   "review_rating", "image_url"]

    categories = all_cats_extractor(SITE_URL)

    for category_url, category_name in zip(categories[0], categories[1]):
        books_urls = product_links_extractor(category_url)
        create_csv(category_name, header_list)
        append_csv(category_name, books_urls)


main()
