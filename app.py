import os
import re
import requests
from newspaper import Article
from bs4 import BeautifulSoup
from flask import Flask, request
from transformers import pipeline


model_name = "deepset/roberta-base-squad2"
model = pipeline('question-answering', model='./model', tokenizer='./model')
 
app = Flask(__name__)


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


@app.route('/predict', methods=['POST'])
def predict():
    return model(request.json)

@app.route('/headlines', methods=['POST'])
def headlines():
    site = request.json.get('site')
    if site:
        url = f'https://www.google.com/search?q={site}&tbm=nws&ei'
    else:
        url = request.json['url']
    headlines, nextp = gnews_get(url)
    return {'headlines': headlines, 'nextpage': nextp}

@app.route('/article', methods=['POST'])
def article():
    url = request.json['url']
    article = Article(url)
    article.download()
    article.parse()
    return {'text': article.text}

if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))