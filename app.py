import os
import re
import requests
from newspaper import Article
from bs4 import BeautifulSoup
from flask import Flask, request
from flask_cors import CORS
from transformers import pipeline
from fake_useragent import UserAgent


model_name = "deepset/roberta-base-squad2"
model = pipeline('question-answering', model='./model', tokenizer='./model')
 
app = Flask(__name__)
CORS(app)


def gnews_get(url):
    list_of_urls = [] 
    page = requests.get(url, headers={'User-Agent': UserAgent().random})
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
    """Predict the answer given a question and context"""

    return model(request.json)

@app.route('/headlines', methods=['POST'])
def headlines():
    """Get the headlines given a search or search url"""

    site = request.json.get('site')
    if site:
        url = f'https://www.google.com/search?q={site}&tbm=nws&ei'
    else:
        url = request.json['url']
    headlines, nextp = gnews_get(url)
    return {'headlines': headlines, 'nextpage': nextp}

@app.route('/article', methods=['POST'])
def article():
    """Get the article content given an article link"""

    url = request.json['url']
    article = Article(url)
    article.download()
    article.parse()
    return {'text': article.text}

if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))