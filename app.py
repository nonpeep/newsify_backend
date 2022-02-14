import csv
import atexit
from datetime import datetime
from flask import Flask, render_template
from .scraper import scrape_all
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

@app.route("/")
def main():
    with open('data.csv','r') as f:
        reader = csv.reader(f)
        data = list(reader)
        data = data[1:]
    news = data
    news = [{"sitename":n[0],"heading": n[1], "summary": n[2], "link": n[3]} for n in news]

    return render_template('index.html', news=news)

scheduler = BackgroundScheduler()
scheduler.add_job(func=scrape_all, trigger="interval", seconds=3600, next_run_time=datetime.now())
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())