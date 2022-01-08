import requests
from bs4 import BeautifulSoup


class BookCategory:
    def __init__(self, category_name, category_url):
        self.category_name = category_name
        self.category_url = category_url
        self.books = []

    def __str__(self):
        return f"The book category is: '{self.category_name}'"

    def soup(self):
        response = requests.get(self.category_url)
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
        return None
