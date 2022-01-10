import csv
import os

import requests
from bs4 import BeautifulSoup

from models.Book import Book
from models.BookCategory import BookCategory

CWD = os.getcwd()
HEADER = ["product_page_url", "universal_product_code", "title",
          "price_including_tax",
          "price_excluding_tax", "number_available",
          "product_description", "category",
          "review_rating", "image_url"]


def create_csv_file(filename, header):
    filepath = os.path.join(CWD + '/data', filename)
    if not os.path.exists(CWD + '/data'):
        os.makedirs(CWD + '/data')
    with open(filepath + '.csv', 'w', encoding="utf-8") as file_csv:
        writer = csv.writer(file_csv,
                            delimiter=',')  # Create writer object
        # with this file
        writer.writerow(header)  # Write the header on first row


def calculate_book_rating(stars):
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
            review_rating = None
    return review_rating


def append_csv_file(filename, books):
    with open('./data/' + filename + '.csv', 'a',
              encoding="utf-8") as file_csv:
        for book in books:
            writer = csv.writer(file_csv, delimiter=',')
            details = (book.book_page_url, book.universal_product_code,
                       book.title, book.price_including_tax,
                       book.price_excluding_tax, book.number_available,
                       book.product_description, book.category,
                       book.review_rating, book.image_url)
            writer.writerow(details)


def download_image_book(image_url, filename):
    invalid = '<>:"/\|?*'
    for char in invalid:
        filename = filename.replace(char, '')
    filename = filename.replace(' ', '_')
    r = requests.get(image_url, allow_redirects=True)
    if not os.path.exists(CWD + './data/images'):
        os.makedirs(CWD + './data/images')
    open('./data/images/' + filename + '.jpg', 'wb').write(r.content)


class Controller:
    def __init__(self, online_resource, info_view):
        self.online_resource = online_resource
        self.info_view = info_view

    def extract_all_categories(self):
        categories = self.online_resource.soup().find('ul',
                                                      class_='nav nav-list').find(
            'ul').findAll('a')
        i = 1
        for category in categories:
            link = category['href']
            full_link = self.online_resource.site_url + link
            cat_name = category.text.strip()
            book_category = BookCategory(cat_name, full_link)
            self.online_resource.book_categories.append(book_category)
            print(f"Cat {i}: {book_category.category_name}")
            i += 1

    def extract_all_books_links(self):
        for category in self.online_resource.book_categories:
            category_url = category.category_url
            cat_url = category_url.rstrip('index.html')
            while True:
                response = requests.get(category_url)
                if response.ok:
                    soup = BeautifulSoup(response.text, 'lxml')
                    books = soup.findAll('article', class_='product_pod')
                    for book in books:
                        link = book.find('a')['href']
                        link = link.strip("./")
                        book_link = self.online_resource.site_url + 'catalogue/' \
                                    + link
                        book_obj = Book(book_link, category.category_name)
                        category.books.append(book_obj)
                    next_page = soup.find('li', class_='next')
                    if not next_page:
                        break
                    next_url = soup.find("li", class_='next').find('a')['href']
                    category_url = cat_url + next_url
                else:
                    return print("url_error")

    def extract_book_data(self):
        for category in self.online_resource.book_categories:
            for book in category.books:
                soup = book.soup()
                table = soup.findAll('td')
                book.universal_product_code = table[0].text

                book.price_including_tax = table[3].text
                book.price_excluding_tax = table[2].text

                stock_txt = table[-2].text
                book.number_available = ''.join(
                    filter(str.isdigit, stock_txt))  # filter out only one
                # number from the string (only works for one number and int)

                book.title = soup.find("h1").text

                product_description = soup.find('div',
                                                id="product_description")
                if not product_description:
                    book.product_description = "No description"
                else:
                    book.product_description = product_description.find_next(
                        'p').text

                stars = soup.find("div", class_="col-sm-6 product_main") \
                    .find("p", class_="star-rating")['class']
                book.review_rating = calculate_book_rating(stars)

                img_url_raw = \
                    soup.find("div", class_="item active").find('img')['src']
                book.image_url = self.online_resource.site_url + \
                                 img_url_raw.strip("./")
                download_image_book(book.image_url, book.title)
                self.info_view.show_book_details(book)

    def load_data_to_csv(self):
        for category in self.online_resource.book_categories:
            create_csv_file(category.category_name, HEADER)
            append_csv_file(category.category_name, category.books)

    def run(self):
        self.info_view.show_status_start()

        self.extract_all_categories()
        self.extract_all_books_links()
        self.extract_book_data()

        self.load_data_to_csv()

        self.info_view.show_status_end()
