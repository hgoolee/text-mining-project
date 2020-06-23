import preprocess as pre
import nltk
from nltk.corpus import sentiwordnet as swn
# import io


class EnglishDictionarySentimentAnalyzer:
    def __init__(self):
        name = 'EnglishDictionarySentimentAnalyzer'

    @staticmethod
    def createDictionary():
        nltk.download('sentiwordnet')


def containKeywords(filterByKeyword, keyword1, keyword2, sentence):
    if not filterByKeyword:
        return True

    for POStag in sentence:
        target = POStag[0].casefold()
        if (keyword1.casefold() in target) or (keyword2.casefold() in target):
            # print("Keywords exist")
            return True
    # print("Keywords do not exist")
    return False


def getSentimentScoreByDocument(doc):
    print("doc: ", end="")
    print(doc)
    sent_sum = 0.0  # document level
    sent_count = 0  # document level
    for sent in doc:
        # print("sent: ", end="")
        # print(sent)
        word_sum = 0.0  # sentence level
        word_count = 0  # sentence level
        for _str in sent:
            # _str[0]
            # _str[1]
            pos = ''
            if str(_str[1]).startswith("N"):
                pos = 'n'
            elif str(_str[1]).startswith("J"):
                pos = 'a'
            elif str(_str[1]).startswith("V"):
                pos = 'v'
            try:
                if len(pos) > 0:
                    score = 0.0
                    breakdown = swn.senti_synset(str(_str[0]) + '.' + pos + '.01')
                    # print("breakdown: ", end="")
                    # print(breakdown)
                    # print("breakdown score: ", end="")
                    # print(str(breakdown) + " " + str(breakdown.pos_score()) + " " +
                    #       str(breakdown.neg_score()) + " " + str(breakdown.obj_score()))
                    if breakdown.pos_score() > breakdown.neg_score():
                        score = breakdown.pos_score()
                        word_count += 1
                    elif (breakdown.pos_score() < breakdown.neg_score()) and (breakdown.neg_score() != 0.0):
                        score = -breakdown.neg_score()
                        word_count += 1
                    word_sum += score
            except nltk.corpus.reader.wordnet.WordNetError:
                pos = ''

        if word_count > 0:
            sent_sum += word_sum / word_count
            sent_count += 1

    return sent_sum, sent_count


# if __name__ == '__main__':
def getSentimentScoreByFile(filePath, windowSize=1, filterByKeyword=False, keyword1=".", keyword2="."):
    if windowSize < 1:
        print("Wrong window size")
        exit(1)

    corpus = pre.CorpusFromFile(filePath)

    pipeline = pre.Pipeline(pre.splitter.NLTK(),
                            # pre.tokenizer.WordPos(),
                            pre.tokenizer.Word(),
                            pre.helper.StopwordFilter(file='../stopwordsEng.txt'),
                            pre.tagger.NLTK(),
                            pre.lemmatizer.WordNet())

    result = pipeline.processCorpus(corpus)
    print(result)

    EnglishDictionarySentimentAnalyzer().createDictionary()

    final_grand_score = 0  # file level
    final_count = 0  # file level
    final_score_array = []  # file level
    for document in result:
        if (windowSize > 1) and (len(document) < windowSize):
            print("Window size is larger than the number of sentences")
            print("Window size will be set as 1 (default) for this document")
            windowSize = 1

        # convertedDocument = document

        if windowSize == 1:
            sentences = [sent for sent in document if containKeywords(filterByKeyword, keyword1, keyword2, sent)]
            # if sentences:  # if sentences list is not empty
            convertedDocument = sentences

        else:  # merge sentences in each document by window size (if windowSize > 1)
            sentences = []
            for sent in document:
                sentences.append(sent)

            newArray = []
            for a in range(0, len(sentences)-windowSize+1):
                middle = int(windowSize/2)
                if containKeywords(filterByKeyword, keyword1, keyword2, sentences[a+middle]):
                    tempArray = [element for b in range(0, windowSize) for element in sentences[a+b]]
                    # tempArray.append(element)
                    # print("tempArray: ", end="")
                    # print(tempArray)
                    newArray.append(tempArray)

            # print("newArray: ", end="")
            # print(newArray)
            # if newArray:  # if newArray list is not empty
            convertedDocument = newArray

        grand_score, count = getSentimentScoreByDocument(convertedDocument)

        if count > 0:
            doc_avg_score = grand_score / count
            print("Average Sentiment Score: " + str(doc_avg_score))
            final_grand_score += doc_avg_score
            final_count += 1
            final_score_array.append(str(doc_avg_score))
        else:
            print("This document is empty")

    try:
        final_avg_score = final_grand_score / final_count
        return str(final_avg_score), final_score_array
    except ZeroDivisionError:
        return str(0), ["This file is empty"]
