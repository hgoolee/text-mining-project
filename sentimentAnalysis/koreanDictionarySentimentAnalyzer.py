# -*- coding: UTF-8 -*-
# import io
# import re


class DictionarySentimentAnalyzer:
    def __init__(self):
        name = 'DictionarySentimentAnalyzer'
        self.dict_list = {}

    def readPolarityDictionary(self, file):
        fh = open(file, mode="r", encoding="utf-8")
        fh.readline()
        for line in fh:
            fields = line.split(',')
            n_token = ''
            toks = fields[0].split(";")
            for tok in toks:
                n_token += tok.split("/")[0]
            print("element " + n_token + " -- " + fields[len(fields)-2] + " : " + fields[len(fields)-1])
            sent_dict = {'word': n_token, 'polarity': fields[len(fields) - 2]}
            if sent_dict['polarity'] is 'NEG':
                sent_dict['score'] = -float(fields[len(fields)-1].replace("\n", ""))
            elif sent_dict['polarity'] is 'POS':
                sent_dict['score'] = float(fields[len(fields) - 1].replace("\n", ""))
            else:
                sent_dict['score'] = 0.0

            if n_token not in self.dict_list:
                self.dict_list[n_token] = sent_dict

    def readKunsanUDictionary(self, file):
        with open(file, encoding='utf-8-sig', mode='r') as f:
            for line in f:
                fields = line.split('\t')
                escaped = fields[0]
                sent_dict = {}
                if len(fields) < 2:
                    continue

                if escaped not in self.dict_list:
                    sent_dict['word'] = escaped
                    sent_dict['score'] = float(fields[1])
                    print('term ' + escaped + " : " + fields[1])
                    if float(fields[1]) < 0:
                        sent_dict['polarity'] = 'NEG'
                    elif float(fields[1]) > 0:
                        sent_dict['polarity'] = 'POS'
                    else:
                        sent_dict['polarity'] = 'NEU'

                    if escaped not in self.dict_list:
                        self.dict_list[escaped] = sent_dict

    def readCurseDictionary(self, file):
        with open(file, encoding='utf-8-sig', mode='r') as f:
            for line in f:
                term = line.strip()
                sent_dict = {}
                if term not in self.dict_list:
                    sent_dict['word'] = term
                    sent_dict['score'] = -2.0
                    print('term ' + term)
                    sent_dict['polarity'] = 'NEG'

                    if term not in self.dict_list:
                        self.dict_list[term] = sent_dict

    def readNegativeDictionary(self, file):
        with open(file, encoding='utf-8-sig', mode='r') as f:
            for line in f:
                term = line.strip()
                sent_dict = {}
                if term not in self.dict_list:
                    sent_dict['word'] = term
                    sent_dict['score'] = -1.0
                    print('term ' + term)
                    sent_dict['polarity'] = 'NEG'

                    self.dict_list[term] = sent_dict

    def readPositiveDictionary(self, file):
        with open(file, encoding='utf-8-sig', mode='r') as f:
            for line in f:
                term = line.strip()
                sent_dict = {}
                if term not in self.dict_list:
                    sent_dict['word'] = term
                    sent_dict['score'] = 1.0
                    print('term ' + term)
                    sent_dict['polarity'] = 'POS'
                    self.dict_list[term] = sent_dict

    def readPositiveEmotiDictionary(self, file):
        with open(file, encoding='utf-8-sig', mode='r') as f:
            for line in f:
                term = line.strip()
                sent_dict = {}
                if term not in self.dict_list:
                    sent_dict['word'] = term
                    sent_dict['score'] = 1.0
                    print('term ' + term)
                    sent_dict['polarity'] = 'POS'
                    self.dict_list[term] = sent_dict

    def readNegativeEmotiDictionary(self, file):
        with open(file, encoding='utf-8-sig', mode='r') as f:
            for line in f:
                term = line.strip()
                sent_dict = {}
                if term not in self.dict_list:
                    sent_dict['word'] = term
                    sent_dict['score'] = -1.0
                    print('term ' + term)
                    sent_dict['polarity'] = 'NEG'
                    self.dict_list[term] = sent_dict

    def getSentiDictionary(self):
        return self.dict_list


if __name__ == '__main__':
    import preprocess as pre
    # import io
    # import nltk

    sentiAnalyzer = DictionarySentimentAnalyzer()

    file_name = './data/SentiWord_Dict.txt'
    sentiAnalyzer.readKunsanUDictionary(file_name)
    file_name = './data/korean_curse_words.txt'
    sentiAnalyzer.readCurseDictionary(file_name)
    file_name = './data/negative_words_ko.txt'
    sentiAnalyzer.readNegativeDictionary(file_name)
    file_name = './data/positive_words_ko.txt'
    sentiAnalyzer.readPositiveDictionary(file_name)
    file_name = './data/emo_negative.txt'
    sentiAnalyzer.readNegativeEmotiDictionary(file_name)
    file_name = './data/emo_positive.txt'
    sentiAnalyzer.readPositiveEmotiDictionary(file_name)
    file_name = './data/polarity.csv'
    sentiAnalyzer.readPolarityDictionary(file_name)

    dict_list = sentiAnalyzer.getSentiDictionary()

    pipeline = None
    # corpus = pre.CorpusFromFieldDelimitedFile('../data/donald.txt', 2)
    mecab_path = 'C:\\mecab\\mecab-ko-dic'
    mode = 'korean_lemmatizer'
    if mode is not 'korean_lemmatizer':
        pipeline = pre.Pipeline(pre.splitter.NLTK(),
                                pre.tokenizer.MeCab(mecab_path),
                                # pre.tokenizer.Komoran(),
                                pre.helper.SelectWordOnly(),
                                pre.ngram.NGramTokenizer(1, 2, concat=' '),
                                pre.helper.StopwordFilter(file='../stopwordsKor.txt'))
    else:
        pipeline = pre.Pipeline(pre.splitter.NLTK(),
                                pre.tokenizer.MeCab(mecab_path),
                                # pre.tokenizer.Komoran(),
                                pre.lemmatizer.SejongPOSLemmatizer(),
                                pre.helper.SelectWordOnly(),
                                # pre.ngram.NGramTokenizer(1, 2, concat=' ')),
                                pre.helper.StopwordFilter(file='../stopwordsKor.txt'))

    # documents = ['오늘은 비가와서 그런지 매우 우울하다',
    #              '시험이 끝나야 놀지 스트레스 받아ㅠㅠ',
    #              '행복한 하루의 끝이라 좋네!',
    #              '더운날에는 아이스커피가 최고지~~']

    documents = ['학기말에 과제가 완전 몰아쳐서 난 요즘 그냥 쥐구멍으로 숨어버리고 싶은 심정이야',
                 '주어진 절대경로와 경로 마지막에 나오는 입력 파일의 이름으로 필요한 디렉토리 정보를 얻으면 된다고 알고 있습니다',
                 '구독자 수 8만 돌파, 여러분 모두 감사해요ㅎㅎ',
                 '할 게 너무 많아서 진짜 힘들긴 하지만 또 다른 한편으로는 정말 재미있는 듯',
                 '그래도 요즘은 출퇴근 안 하고 재택 근무하니 좋은 점도 상당히 많은 거 같죠?ㅋㅋㅋㅋ']

    # result = pipeline.processCorpus(corpus)
    # print(len(corpus.docs))
    result = pipeline.processCorpus(documents)
    print(result)

    for doc in result:
        total_score = 0.0
        count = 0
        for sent in doc:
            for _str in sent:
                if len(_str) > 0:
                    score = 0.0
                    dictionary_ele = dict_list.get(_str)
                    if dictionary_ele is not None:
                        polarity = dictionary_ele.get('polarity')
                        score = float(dictionary_ele.get('score'))
                        count += 1
                        # print(_str + " == " + polarity + " " + str(score))
                        total_score += score
                    else:
                        total_score += score

        if count != 0:
            avg_score = total_score / count
            print("AVG SCORE " + str(avg_score))
