from mongo.mongo import *
from mongoengine import *
import datetime


def insert_data(source):
    database = connect("news_scraping", host="localhost", port=27017)

    num_articles = Article.objects.count() + 1

    filePath = "./data/" + source + "_date_content.txt"
    file = open(filePath, "r", encoding="utf8")
    for each in file:
        line = each.split('\t')
        lineDate = line[0]
        lineContent = line[1]
        lineSource = source

        year = lineDate[0:4]
        month = lineDate[5:7]
        day = lineDate[8:10]

        article = Article(_id=num_articles,
                          date=datetime.datetime(int(year), int(month), int(day)),
                          content=lineContent,
                          source=lineSource)
        article.save()

        num_articles += 1

    file.close()
    disconnect()


# TODO: Choose sources to insert into MongoDB
dataArray = ["Chicago Tribune"]

for data in dataArray:
    print("Data being inserted!\n")
    insert_data(data)
