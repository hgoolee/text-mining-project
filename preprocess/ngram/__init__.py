from itertools import chain

class BaseNgram:
    IN_TYPE = [list, str]
    OUT_TYPE = [list, str]

class NGramTokenizer(BaseNgram):

    def __init__(self, min=1, max=2):  #ngramCount=(1,2)  # default는 unigram부터 시작
        self.ngramCount = max
        self.min = min

    def __call__(self, *args, **kwargs):
        converted = []
        from nltk.util import ngrams
        for i in range(self.min, self.ngramCount+1):
            output = list(ngrams((args[0]), i))
            for x in output:
                if (len(x) > 0):
                    converted.append("_".join(x))

        #print("NGRAM " + str(converted))

        return converted