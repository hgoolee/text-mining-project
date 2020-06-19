# testCooccurrence.py modified

# -*- encoding:utf8 -*-
import preprocess as pre
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib as mpl

if __name__ == '__main__':

    corpus = pre.CorpusFromFieldDelimitedFile('../data/ALLre_date_content.txt',1)

    pipeline = pre.Pipeline(pre.splitter.NLTK(),
                            pre.tokenizer.WordPos(),
                            pre.lemmatizer.WordNet(),
                            pre.helper.POSFilter('N*', 'V*', 'J*'),
                            pre.helper.SelectWordOnly(),
                            pre.helper.StopwordFilter(file='../stopwordsEng.txt'))
#                            pre.ngram.NGramTokenizer(1, 2))

    result = pipeline.processCorpus(corpus)
    print('== 전처리 완료 ==')
    print(result)
    print()

    file=open('ALLre_all_AVJ_pre.txt', 'w')
    file.write(result)
    file.close()

    print('==  ==')

    documents = []
    for doc in result:
        document = ''
        for sent in doc:
            document = " ".join(sent)
        documents.append(document)

    co = pre.cooccurrence.CooccurrenceWorker()
    co_result, vocab = co.__call__(documents)

    graph_builder = pre.graphml.GraphMLCreator()

    # mode is either with_threshold or without_threshod
    mode = 'with_threshold'

    if mode is 'with_threshold':
        cv = CountVectorizer()
        cv_fit = cv.fit_transform(documents)
        word_list = cv.get_feature_names();
        count_list = cv_fit.toarray().sum(axis=0)
        word_hist = dict(zip(word_list, count_list))

        graph_builder.createGraphMLWithThreshold(co_result, word_hist, vocab, "ALLre_all_NVJ.graphml",threshold=16)
        print("complete!")
