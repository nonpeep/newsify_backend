from bs4 import BeautifulSoup
import requests
import re


def gnews_get(url):
    list_of_urls = [] 
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    article_div = soup.find_all('a')
    for a in article_div:
        if 'google' not in str(a):
            link = re.findall('https[\S]+' ,a['href'])
        if a.text != '':
            try:
                end_index = link[0].find('&')
                link = link[0][0:end_index]
                list_of_urls.append((a.find('div').text, link))
            except:
                continue
    
    nextpage = soup.find(attrs={"aria-label": "Next page"})['href']
    return list_of_urls, f'https://www.google.com{nextpage}'