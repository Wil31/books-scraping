import requests
from bs4 import BeautifulSoup
import csv
import re


# Extract a list of data from a specific book url
def extractor(url):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')

        product_page_url = url
        table = soup.findAll('td')
        universal_product_code = table[0].text

        price_including_tax = table[3].text
        price_including_tax = re.findall(r"[-+]?\d*\.\d+|\d+", price_including_tax)  # regular
        # expression operation to return all non-overlapping matches from the pattern
        # "[-+]?\d*\.\d+|\d+"
        price_including_tax = ''.join(map(str, price_including_tax))  # map() to convert each item in
        # the list to a string, and then join them

        price_excluding_tax = table[2].text
        price_excluding_tax = re.findall(r"[-+]?\d*\.\d+|\d+", price_excluding_tax)
        price_excluding_tax = ''.join(map(str, price_excluding_tax))

        stock_txt = table[-2].text
        number_available = ''.join(filter(str.isdigit, stock_txt))  # filter out only one number from
        # the string (only works for one number and int)

        title = soup.find("h1").text

        product_description = soup.find('div', id="product_description").find_next('p').text

        category = soup.find("ul", "breadcrumb").find_next("a").find_next("a").find_next("a").text

        stars = soup.find("div", class_="col-sm-6 product_main").find("p", class_="star-rating")['class']
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

        image_url = 'https://books.toscrape.com/' + soup.find("div", class_="item active").find('img')['src']

        #  Create a list with the data extracted from product page
        book_extract = [product_page_url, universal_product_code, title, price_including_tax,
                        price_excluding_tax, number_available, product_description, category,
                        review_rating, image_url]
        return book_extract
    else:
        return "url error"


# Create file data.csv and input the header
def create_csv(header):
    with open('data.csv', 'w', encoding="utf-8") as file_csv:
        writer = csv.writer(file_csv, delimiter=',')  # Create writer object with this file
        writer.writerow(header)  # Write the header on first row


# Append a new row in data.csv file
def append_csv(row):
    with open('data.csv', 'a', encoding="utf-8") as file_csv:
        writer = csv.writer(file_csv, delimiter=',')
        writer.writerow(row)  # Append with the new row


book_url = 'https://books.toscrape.com/catalogue/follow-you-home_809/index.html'

# Header list for the csv file
header_list = ["product_page_url", "universal_product_code", "title", "price_including_tax",
               "price_excluding_tax", "number_available", "product_description", "category",
               "review_rating", "image_url"]
create_csv(header_list)
append_csv(extractor(book_url))
