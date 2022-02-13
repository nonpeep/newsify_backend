from flask import Flask, render_template
from .scraper import TheHindu

app = Flask(__name__)

@app.route("/")
def hello_world():
    news = TheHindu().get_news()
    news = [{"heading": n[0], "summary": n[1], "link": n[2], "sitename":"The Hindu"} for n in news]
    return render_template('index.html', news=news)