# -*- encoding:utf8 -*-
import preprocess as pre
from controlDB import *
from mongoengine import *
import datetime
import os


# Filter news articles by date range from MongoDB
def filter_by_date_range(startDate, endDate):
    connect("news_scraping", host="localhost", port=27017)

    articles = Article.objects(Q(date__gte=startDate) & Q(date__lte=endDate))

    filePath = "./data/date_from" + startDate.strftime("%Y%m%d") + "to" + endDate.strftime("%Y%m%d") + "_data.txt"
    file = open(filePath, "w", encoding='utf8')

    print("Total of %d documents\n" % articles.count())
    print("List of articles:", articles, "\n")
    count = 1
    for article in articles:
        file.write(article.content)
        print("article", count, ": ", article.content, sep="")
        count += 1

    file.close()
    disconnect()


# Pre-process news articles by date range
def process_by_date_range(startDate, endDate):
    filter_by_date_range(startDate, endDate)

    user_dict = './user_dic.txt'

    # TODO: Customize pre-processing pipeline
    pipeline = pre.Pipeline(pre.splitter.NLTK(),
                            pre.tokenizer.WordPos(),
                            pre.lemmatizer.WordNet(),
                            pre.helper.POSFilter('N*|J*|R*|V*'),
                            pre.helper.SelectWordOnly(),
                            pre.helper.StopwordFilter(file='./stopwordsEng.txt'),
                            pre.ngram.NGramTokenizer(1, 2),
                            pre.counter.WordCounter())

    filePath1 = "./data/date_from" + startDate.strftime("%Y%m%d") + "to" + endDate.strftime("%Y%m%d") + "_data.txt"

    corpus = pre.CorpusFromFieldDelimitedFile(filePath1, 0)

    if os.path.exists(filePath1):
        # os.remove(filePath1)
        print(filePath1, "is now being processed!\n")
    else:
        print("File does not exist!")

    result = pipeline.processCorpus(corpus)

    print(result)
    print()

    doc_collection = ''
    term_counts = {}
    for doc in result:
        for sent in doc:
            for _str in sent:
                term_counts[_str[0]] = term_counts.get(_str[0], 0) + int(_str[1])
                freq = range(int(_str[1]))
                co = ''
                for n in freq:
                    co += ' ' + _str[0]

                doc_collection += ' ' + co

    word_freq = []
    for key, value in term_counts.items():
        word_freq.append((value, key))

    word_freq.sort(reverse=True)
    print(word_freq)

    filePath2 = "./result/date_from" + startDate.strftime("%Y%m%d") + "to" + endDate.strftime("%Y%m%d") + "_result.txt"

    f = open(filePath2, "w", encoding='utf8')
    for pair in word_freq:
        f.write(pair[1] + '\t' + str(pair[0]) + '\n')
    f.close()

    return doc_collection
