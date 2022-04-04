import os
import re
import requests
from newspaper import Article
from flask import Flask, request
from flask_cors import CORS
from transformers import pipeline

model_name = "deepset/roberta-base-squad2"
model = pipeline('question-answering', model='./model', tokenizer='./model')
 
app = Flask(__name__)
CORS(app)


@app.route('/predict', methods=['POST'])
def predict():
    """Predict the answer given a question and context"""

    return model(request.json)

@app.route('/headlines', methods=['GET', 'POST'])
def headlines():
    """Get the headlines given a search or search url"""

    params = {
        "language": "en",
        "apiKey": os.environ.get("API_KEY"),
        "pageSize": 100
    }
    if request.json:
        params.update(request.json)
    response = requests.get("https://newsapi.org/v2/top-headlines", params=params)
    headlines = response.json()
    return headlines

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