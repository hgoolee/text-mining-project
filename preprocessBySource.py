# -*- encoding:utf8 -*-
import preprocess as pre
from controlDB import *
from mongoengine import *
import os


# Filter news articles by source from MongoDB
def filter_by_source(source):
    connect("news_scraping", host="localhost", port=27017)

    articles = Article.objects(source=source)

    filePath = "./data/" + source + "_data.txt"
    file = open(filePath, "w", encoding='utf8')

    print("Total of %d documents\n" % articles.count())
    for article in articles:
        file.write(article.content)
        print(article.content)

    file.close()
    disconnect()


# Pre-process news articles by source
def process_by_source(source):
    filter_by_source(source)

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

    filePath1 = "./data/" + source + "_data.txt"

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

    filePath2 = "./result/source_" + source + "_result.txt"

    f = open(filePath2, "w", encoding='utf8')
    for pair in word_freq:
        f.write(pair[1] + '\t' + str(pair[0]) + '\n')
    f.close()

    return doc_collection
