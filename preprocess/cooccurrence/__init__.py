import string
from collections import Counter
import os
from nltk import bigrams
from collections import defaultdict
import operator
import numpy as np

class BaseCooccurrence:
    INPUT=[list,str]
    OUTPUT=[list,tuple]

# tuple. vectorize. 실수값.
class CooccurrenceWorker(BaseCooccurrence):
    def __init__(self):
        name = 'cooccurrence'

        from sklearn.feature_extraction.text import CountVectorizer
        import preprocess.cooccurrence.cooccurrence as co
        self.inst = co.Cooccurrence(ngram_range=(2, 2), stop_words='english')

    def __call__(self, *args, **kwargs):


        # bigram_vectorizer = CountVectorizer(ngram_range=(1, 2), vocabulary={'awesome unicorns': 0, 'batman forever': 1})
    # transpose한 line. 결과로 텀텀 매트릭스 떨어짐. (sparse->dense).
        co_occurrences = self.inst.fit_transform(args[0])
        # print('Printing sparse matrix:', co_occurrences)
        # print(co_occurrences.todense())
    #더 dense하게 하기 위해서 카운터벡터라이저의 todense.
        sum_occ = np.sum(co_occurrences.todense(), axis=0)
        # print('Sum of word-word occurrences:', sum_occ)

        # Converting itertor to set
    #iterater->set->list. bcs 얘의 caller가 testcooccurence co.__call(documents). 얘는 문헌집단(문헌 arrya) 받는 애임. -> co_result, vocab리턴.
        result = zip(self.inst.get_feature_names(), np.array(sum_occ)[0].tolist())
        result_set = list(result)
        return result_set, self.inst.vocab()

# Co-occurence count
#매트릭스 아니라 그냥 코어커 센거니까. 값이 그냥 정수값int.
class CooccurrenceManager:
    def computeCooccurence(self, list):
        com = defaultdict(lambda: defaultdict(int))
        count_all = Counter()
        count_all1 = Counter()

        uniqueList = []
        for _array in list:
            for line in _array:
                for word in line:
                    if word not in uniqueList:
                        uniqueList.append(word)

                terms_bigram = bigrams(line)
                # Update the counter
                count_all.update(line)
                count_all1.update(terms_bigram)

                # Build co-occurrence matrix
                for i in range(len(line) - 1):
                    for j in range(i + 1, len(line)):
                        w1, w2 = sorted([line[i], line[j]])
                        if w1 != w2:
                            com[w1][w2] += 1

        com_max = []
        # For each term, look for the most common co-occurrent terms
        for t1 in com:
            t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
            for t2, t2_count in t1_max_terms:
                com_max.append(((t1, t2), t2_count))
        # Get the most frequent co-occurrences
        terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)

        return terms_max, uniqueList

