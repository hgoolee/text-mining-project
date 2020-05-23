''' str => list(str) '''

class BaseTokenizer:
    IN_TYPE = [str]
    OUT_TYPE = [list, str]

# [English]
class Tweet(BaseTokenizer):
    def __init__(self):
        import nltk.tokenize
        self.inst = nltk.tokenize.TweetTokenizer()

    def __call__(self, *args, **kwargs):
        return self.inst.tokenize(*args)

class Whitespace(BaseTokenizer):
    def __init__(self):
        import nltk.tokenize
        self.inst = nltk.tokenize.WhitespaceTokenizer()

    def __call__(self, *args, **kwargs):
        return self.inst.tokenize(*args)

class Word(BaseTokenizer):
    def __init__(self):
        import nltk.tokenize
        self.inst = nltk.tokenize.word_tokenize

    def __call__(self, *args, **kwargs):
        return self.inst(*args)

# [English]
class WordPos(BaseTokenizer):
    def __init__(self):
        import nltk
        self.inst = nltk
        self.OUT_TYPE = (list, tuple)  # output type은 (단어, 품사)로 이루어짐

    def __call__(self, *args, **kwargs):
        tokens = self.inst.word_tokenize(*args)  # 1) 문장이나 문헌이 들어오면 tokenize

        return self.inst.pos_tag(tokens)  # 2) token array를 input으로 받아서 단어와 그 단어의 품사르 return

# [Korean]
class Komoran(BaseTokenizer):
    def __init__(self,userdic=None):
        from konlpy.tag import Komoran
        import os
        if userdic is not None:
            print("user dict " + str(os.path.abspath(userdic)))
            self.inst = Komoran(userdic=os.path.abspath(userdic))
        else:
            self.inst = Komoran()
        self.OUT_TYPE = [list, tuple]

    def __call__(self, *args, **kwargs):
        return self.inst.pos(args[0])

class TwitterKorean(BaseTokenizer):
    def __init__(self):
        from konlpy.tag import Twitter
        self.inst = Twitter()

        self.OUT_TYPE = [list, tuple]

    def __call__(self, *args, **kwargs):
        return self.inst.pos(args[0])

class KokomaKorean(BaseTokenizer):
    def __init__(self):
        from konlpy.tag import Kkma
        self.inst = Kkma()

        self.OUT_TYPE = [list, tuple]

    def __call__(self, *args, **kwargs):
        return self.inst.pos(args[0])

class SpecialTokenizer:
    IN_TYPE = [str]
    OUT_TYPE = [str]

class MaxScoreTokenizerKorean(SpecialTokenizer):
    def __init__(self, scores=None):
        from soynlp.tokenizer import MaxScoreTokenizer
        self.inst=MaxScoreTokenizer(scores=scores)
        self.OUT_TYPE = [list, str]

    def __call__(self, *args, **kwargs):
        tokens = self.inst.tokenize(args[0])
        return tokens

class LTokenizerKorean(SpecialTokenizer):  # 어근 중심 tokenizer
    def __init__(self, scores=None):
        from soynlp.tokenizer import LTokenizer
        self.inst=LTokenizer(scores=scores)  # scores를 preference로 지정할 수 있고, 지정하지 않으면 cohesion score로 알아서 계산됨
        self.OUT_TYPE = [list, str]

    def __call__(self, *args, **kwargs):
        tokens = self.inst.tokenize(args[0])
        return tokens

class RegexTokenizerKorean(SpecialTokenizer):
    def __init__(self):
        from soynlp.tokenizer import RegexTokenizer
        self.inst=RegexTokenizer()
        self.OUT_TYPE = [list, str]

    def __call__(self, *args, **kwargs):
        tokens = self.inst.tokenize(args[0])
        return tokens

class MeCab(BaseTokenizer):
    def __init__(self, path=None):
        #import MeCab
        #self.inst = MeCab.Tagger()
        from konlpy.tag import Mecab
        self.inst = Mecab(path)   # path is user defined dictionary

        self.OUT_TYPE = [list, tuple]

    def __call__(self, *args, **kwargs):
        return self.inst.pos(args[0])  # args[0] (= sentence) 내의 각각 단어의 품사를 태깅해서 return
