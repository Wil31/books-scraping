import requests
from bs4 import BeautifulSoup


class OnlineResource:
    def __init__(self, site_url):
        self.site_url = site_url
        self.book_categories = []

    def __str__(self):
        return f"The resource url is: '{self.site_url}'"

    def soup(self):
        response = requests.get(self.site_url)
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
        return None
