import re
import csv
import requests
from .similarity import get_unique
from bs4 import BeautifulSoup


def store_csv(data):
    """Stores the news in a csv file"""
    
    filename = "./data.csv"
    fields = ['Site name', 'Headline', 'Summary', 'Link']
    with open(filename, 'w', encoding="utf-8", newline="") as csvfile:  
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(data)

def scrape_all():
    """Scrapes from all known sites."""

    print("Starting scraper...")
    scrapers = [TheHindu(), NDTV()]
    news = [scraper.get_news() for scraper in scrapers]
    print("Removing duplicates...")
    news = get_unique(news)
    store_csv(news)
    print("Data stored on data.csv file")


class Scraper():
    """Parent class for specific news site scrapers."""

    def get_articles(self) -> list:
        """Returns a list of tuples formatted as (headline, link)."""
        pass

    def get_article_content(self, article_url) -> str:
        """Gets the article content from the url."""
        pass

    def get_news(self) -> list:
        """Get the current news, returns a list of tuples (sitename, headline, content, link)"""

        articles = self.get_articles()
        return [(self.site_name, a[0], self.get_article_content(a[1]), a[1]) for a in articles]


class TheHindu(Scraper):
    site_name = 'The Hindu'
    url = 'https://www.thehindu.com/'

    def get_articles(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, "html.parser")
        articles = soup.find_all(class_="e-p-slide")
        gettext = lambda x: x.text.partition('|')[2].strip()
        return [(gettext(art.div.a), art.div.a['href']) for art in articles]
    
    def get_article_content(self, article_url):
        page = requests.get(article_url)
        soup = BeautifulSoup(page.text, "html.parser")
        id_of_content = re.findall('content[-]body[-][0-9]+', page.text)
        article_div = soup.find_all(id= id_of_content)
        return article_div[0].text


class NDTV(Scraper):
    site_name = 'NDTV'
    url = 'https://www.ndtv.com/india/'

    def get_articles(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, "html.parser")
        articles = soup.find_all(class_ = "news_Itm-cont")

        return [(art.a.text, art.a['href']) for art in articles]

    def get_article_content(self, article_url):
        page = requests.get(article_url)
        soup = BeautifulSoup(page.text, "html.parser")
        article_div = soup.find_all(id= 'ins_storybody')
        return article_div[0].text
