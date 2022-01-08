from controllers.Controller import Controller
from models.OnlineResource import OnlineResource
from views.InfoView import InfoView

SITE_URL = 'https://books.toscrape.com/'


def main():
    online_resource = OnlineResource(SITE_URL)
    info_view = InfoView()

    extract = Controller(online_resource, info_view)
    extract.run()


if __name__ == "__main__":
    main()
