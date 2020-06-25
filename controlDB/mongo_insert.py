from controlDB.mongo import *
from mongoengine import *
import datetime
import re


def insert_data(source):
    database = connect("news_scraping", host="localhost", port=27017)

    num_articles = Article.objects.count() + 1
    lineCount = 1

    filePath = "../data/original/" + source + "_date_content.txt"
    file = open(filePath, "r", encoding="utf8")

    for each in file:
        line = each.split('\t')

        if len(line) == 2:
            if re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", line[0]):
                # print("Line", lineCount, "in", source, "is being inserted!\n")

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
            else:
                print("Line ", lineCount, " in ", source, ": date format not supported\n", sep="")
        else:
            print("Line ", lineCount, " in ", source, ": line format not supported\n", sep="")

        lineCount += 1

    file.close()
    disconnect()


# TODO: Choose sources to insert into MongoDB
dataArray = ["Chicago Tribune", "CNN", "Los Angeles Times", "New York Times",
             "USA Today, CBS, Fox", "Wall Street Journal", "Washington Post"]

for data in dataArray:
    try:
        insert_data(data)
        print(data, "has been successfully inserted!\n")
    except FileNotFoundError:
        print(data, "does not exist in this folder!\n")
        continue
