import requests
from bs4 import BeautifulSoup


class Book:
    def __init__(self, book_page_url, category):
        self.book_page_url = book_page_url
        self.category = category
        self.universal_product_code = None
        self.title = None
        self.price_including_tax = None
        self.price_excluding_tax = None
        self.number_available = None
        self.review_rating = None
        self.product_description = None
        self.image_url = None

    def __str__(self):
        return f"The book title is: '{self.title}',\n" \
               f"url: {self.book_page_url},\n" \
               f"cat: {self.category},\n" \
               f"UPC: {self.universal_product_code},\n" \
               f"price /w tax: {self.price_including_tax},\n" \
               f"price /wo tax: {self.price_excluding_tax},\n" \
               f"number available: {self.number_available},\n" \
               f"rating: {self.review_rating},\n" \
               f"description: {self.product_description}"

    def __repr__(self):
        """Used in print."""
        return str(self)

    def soup(self):
        response = requests.get(self.book_page_url)
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
        return None
