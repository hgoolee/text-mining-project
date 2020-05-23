# -*- encoding:utf8 -*-
import preprocess as pre

user_dict = './user_dic.txt'

pipeline = pre.Pipeline(pre.splitter.NLTK(),
                        pre.tokenizer.WordPos(),
                        pre.helper.POSFilter('N*|J*|R*|V*'),
                        pre.helper.SelectWordOnly(),
                        pre.helper.StopwordFilter(file='./stopwordsEng.txt'),
                        pre.counter.WordCounter())

corpus = pre.CorpusFromFieldDelimitedFile('./data/sampleEng.txt', 0)

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
    word_freq.append((value,key))

word_freq.sort(reverse=True)
print(word_freq)

f = open("demo_result.txt", "w", encoding='utf8')
for pair in word_freq:
    f.write(pair[1] + '\t' + str(pair[0]) + '\n')
f.close()

from wordcloud import WordCloud

wordcloud = WordCloud().generate(doc_collection)

import matplotlib.pyplot as plt

wordcloud = WordCloud(max_font_size=40,
                      background_color='white',
                      collocations=False,
                      font_path='C:/Windows/Fonts/malgun.ttf').generate(doc_collection)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
