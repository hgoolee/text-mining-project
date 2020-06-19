import numpy as np
import scipy.sparse as sp
from sklearn.feature_extraction.text import CountVectorizer

#CountVectorizer inherit. 오버라이딩.
class Cooccurrence(CountVectorizer):
    """Co-ocurrence matrix
    Convert collection of raw documents to word-word co-ocurrence matrix

    Parameters
    ----------
    encoding : string, 'utf-8' by default.
        If bytes or files are given to analyze, this encoding is used to
        decode.

    ngram_range : tuple (min_n, max_n)
        The lower and upper boundary of the range of n-values for different
        n-grams to be extracted. All values of n such that min_n <= n <= max_n
        will be used.

    max_df: float in range [0, 1] or int, default=1.0

    min_df: float in range [0, 1] or int, default=1

    Example
    -------

    >> import Cooccurrence
    >> docs = ['this book is good',
               'this cat is good',
               'cat is good shit']
    >> model = Cooccurrence()
    >> Xc = model.fit_transform(docs)

    Check vocabulary by printing
    >> model.vocabulary_

    """

    def __init__(self, encoding='utf-8', ngram_range=(1, 1),
                 max_df=1.0, min_df=1, max_features=None,
                 stop_words=None, normalize=True, vocabulary=None):

        #카운트 벡터라이저 사용하여 전체 문헌집단의 빈도수 계산.
        super(Cooccurrence, self).__init__(
            ngram_range=ngram_range,
            max_df=max_df,
            min_df=min_df,
            max_features=max_features,
            stop_words=stop_words,
            vocabulary=vocabulary
        )

        self.X = None

        self.normalize = normalize

    #오버라이딩. 카운트벡터라이저는 '단어의 빈도수' 계산. 여기서는 '두 단어의 빈도수' 계산. by matrix
    # 코어커 계산: init 1st.Worker by matrix // init 2nd.Manager 페어의 코어커. json매트릭스... (매트릭스이긴 한데 이건 그냥 페어의 동시출현 구하는 거임.)
    #유닉텀.카운트나오는 매트릭스.벡터라이즈.이거 가지고는 구할 수 없으니까 다큐먼트 매트릭스(가로는 doc, 세로는 term, 셀에 count.)-> 텀텀 매트릭스.by SVD.~ 동시출현쌍 그릴 수 있음.
    #이때 x,y 둘 다 텀이니까, 대각선(diagonal)그려서 한쪽만 구해도 충분함.(위나 아래나...같은 값이 있을 것.)

    def fit_transform(self, raw_documents, y=None):
        """Fit cooccurrence matrix

        Parameters
        ----------
        raw_documents : iterable
            an iterable which yields either str, unicode or file objects

        Returns
        -------
        Xc : Cooccurrence matrix

        """
        #카운트 벡터라이즈에서 X는 결과값. 단어와 단어의 빈도로 이루어진 dictionary list.
        #'super'니까 카운트벡터라이저겠지?
        X = super(Cooccurrence, self).fit_transform(raw_documents)
        self.X = X

        n_samples, n_features = X.shape

    #transform. decompose. : 실수값으로 됨. count값 아니라 근사값 나옴. 실제로 센 게 아니라 matrix transpose한 것이기 때문.
        Xc = (X.T * X)
        if self.normalize:
            g = sp.diags(1./Xc.diagonal())
            Xc = g * Xc
        else:
            Xc.setdiag(0)

        return Xc

    #unique한 단어 list return
    def vocab(self):
        tuples = super(Cooccurrence, self).get_feature_names()
        vocabulary=[]
        for e_tuple in tuples:
            tokens = e_tuple.split()
            for t in tokens:
                if t not in vocabulary:
                    vocabulary.append(t)

        return vocabulary

    #unique단어 list+출현빈도. histgram return
    def word_histgram(self):
        word_list = super(Cooccurrence, self).get_feature_names()
        count_list = self.X.toarray().sum(axis=0)
        return dict(zip(word_list,count_list))