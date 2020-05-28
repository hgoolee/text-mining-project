from mongo import *
from mongoengine import *
import datetime

# Choose a date
year = "2020"
month = "05"
day = "15"

connect("news_scraping", host="localhost", port=27017)

articles = Article.objects(date=datetime.datetime(2020, 5, 15))

articles.update(
    category="mask",
    sentiment=Sentiment(positive=60, negative=30, neutral=10)
)

disconnect()
