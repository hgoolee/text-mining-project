from controlDB import *
from mongoengine import *
from sentimentAnalysis.englishDictionarySentimentAnalyzer2 import *
import datetime
import os

# TODO: Choose a range of dates to calculate sentiment score
startYear = "2020"
startMonth = "01"
startDay = "01"

endYear = "2020"
endMonth = "02"
endDay = "18"

# TODO: You may change the size of the window
windowSize = 7

# TODO: You may select only sentences that contain specific keywords (case-insensitive)
filterByKeyword = True
keyword1 = "Korea"
keyword2 = "Korea"


# Filter news articles by date from MongoDB
def filter_by_date(year, month, day):
    connect("news_scraping", host="localhost", port=27017)

    articles = Article.objects(date=datetime.datetime(int(year), int(month), int(day)))
    print("Total of %d document(s)\n" % articles.count())
    # print("List of articles:", articles, "\n")

    filePath = "../data/[Sentiment]date_" + year + month + day + "_data.txt"
    file = open(filePath, "w", encoding='utf-8')

    i = 1
    for article in articles:
        file.write(article.content)
        print("article", i, ": ", article.content, sep="")
        i += 1

    file.close()
    disconnect()

    return filePath


if __name__ == "__main__":
    start_date = datetime.datetime(int(startYear), int(startMonth), int(startDay))
    end_date = datetime.datetime(int(endYear), int(endMonth), int(endDay))
    one_day = datetime.timedelta(days=1)

    scoreArray = []
    current_date = start_date
    while current_date <= end_date:
        dateFilePath = filter_by_date(str(current_date.year),
                                      str(current_date.month).zfill(2),
                                      str(current_date.day).zfill(2))
        if os.path.exists(dateFilePath):
            average_score, all_scores = getSentimentScoreByFile(dateFilePath,
                                                                windowSize,
                                                                filterByKeyword,
                                                                keyword1,
                                                                keyword2)
            scoreArray.append([current_date.strftime("%Y-%m-%d"), average_score, "/".join(all_scores)])
            os.remove(dateFilePath)
        else:
            print("File does not exist!")
            exit(1)
        current_date += one_day

    scoreFilePath = "../result/[Sentiment-" + str(windowSize) + "]date_from" +\
                    start_date.strftime("%Y%m%d") + "to" + end_date.strftime("%Y%m%d") +\
                    "_result.txt"
    with open(scoreFilePath, "w", encoding='utf-8') as scoreFile:
        for element in scoreArray:
            line = "\t".join(element) + "\n"
            scoreFile.write(line)
