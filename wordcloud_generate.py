from test1 import *
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Generate Word Cloud
# TODO: MUST refer to test1.py file
wordcloud = WordCloud().generate(doc_collection)

wordcloud = WordCloud(max_font_size=40,
                      background_color='white',
                      collocations=False,
                      font_path='C:/Windows/Fonts/malgun.ttf').generate(doc_collection)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
