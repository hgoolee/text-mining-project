# -*- encoding:utf8 -*-
import preprocess as pre
from mongo.mongo import *
from mongoengine import *
import datetime
import os


# Get news articles from MongoDB by date
def get_by_date(year, month, day):
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


# TODO: Choose a date to extract news articles
year = "2020"
month = "05"
day = "15"

get_by_date(year, month, day)

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

filePath1 = "./data/" + year + month + day + "_data.txt"

corpus = pre.CorpusFromFieldDelimitedFile(filePath1, 0)

if os.path.exists(filePath1):
    os.remove(filePath1)
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

filePath2 = "./result/" + year + month + day + "_result.txt"

f = open(filePath2, "w", encoding='utf8')
for pair in word_freq:
    f.write(pair[1] + '\t' + str(pair[0]) + '\n')
f.close()
