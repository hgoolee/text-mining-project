from mongo.mongo import *
from mongoengine import *
import datetime

# Choose a date
year = "2020"
month = "05"
day = "15"

connect("news_scraping", host="localhost", port=27017)

articles = Article.objects(date=datetime.datetime(int(year), int(month), int(day)))

filePath = "./data/" + year + month + day + "_data.txt"
file = open(filePath, "w", encoding='utf8')

print("Total of %d documents\n" % articles.count())
for article in articles:
    file.write(article.content)
    print(article.content)

file.close()
disconnect()
