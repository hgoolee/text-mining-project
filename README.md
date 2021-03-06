# Text Mining Final Project - Group 1 (completed)

## Our schedule (tentative)
- [x] Getting Started
- [x] Scraping
- [x] Data Pre-processing
- [x] Count Occurrence (Word Cloud)
- [x] Co-occurrence
- [x] Sentiment Analysis
- [x] Topic Modelling
- [x] Result Interpretation
- [x] Visualization

## Major Changes & Updates
*  ALL MAJOR CHANGES MUST BE CLEARLY EXPLAINED IN THIS FILE
* ***It is strongly recommended to follow the format of this file***

### 0528
1. 프로젝트를 MongoDB에 연결하고 `mongo` 폴더에 해당되는 파일 추가(5개)
1. `preprocess` 폴더에 *ngram*과 *tagger* 추가
1. `data` 폴더에 신문기사 원본 파일 추가(7개)
1. `result` 폴더 추가(전처리가 완료된 신문기사를 저장할 폴더)
1. `test1.py` 수정 - 신문기사를 날짜 별로 분리할 수 있도록 함
1. `test2.py` 추가(pymongo 연습용) - 사용하지 않음
1. `wordcloud_generate.py` 추가(기존 `test1.py`에서 Word Cloud 부분 분리)
1. `HISTORY.txt` 추가

### 0530
1. updated `data` files, according to the form
1. moved `data` files that are not directly related to our project into a lower-level folder
1. updated `stopwordsEng.txt`
1. moved `test1.py` file into `mongo` folder
1. created `README.md`

### 0601
1. renamed `mongo` folder to `controlDB`
1. resolved import error by adding `__init__.py` file to `controlDB` folder
1. added `preprocessByDate.py`, `preprocessByCategory.py`, `preprocessBySource.py` files
1. enabled additional features in `test1.py`
   * pre-process by *date*(a range of dates instead of a single date) - when *mode* is 1
   * pre-process by *category* - when *mode* is 2
   * pre-process by *source* - when *mode* is 3
   * generate Word Cloud - when *generateWordCloud* is True
1. updated `wordcloud_generate.py`
1. edited `README.md` - made the format more organised
1. removed `HISTORY.txt`
1. renamed `+a` folder to `sample`

### 0607
1. created `preprocessByDateRange.py`
1. enabled additional features in `test1.py`
   * pre-process by *date range* - when *mode* is 1
     * output TWO files in total
     * output a SINGLE file consisting of all news articles of the given date range
     * output a SINGLE file consisting of pre-processed result of the given date range
1. updated mode number in `test1.py`
    * pre-process by *date* - when *mode* is 2
    * pre-process by *category* - when *mode* is 3
    * pre-process by *source* - when *mode* is 4

### 0611
1. created `sentimentAnalysis` folder and added `englishDictionarySentimentAnalyzer.py`
1. created `preprocessByKeyword.py`
1. added additional features to `test1.py`
   * pre-process by *keyword* - when *mode* is 5
1. created `countWordOccurrence.py`
   * count the occurrence of the given substring in each article
1. created `WebScraper` folder and added `collector` module - not going to be used

### 0618
1. added files in `sentimentAnalysis` folder from our original module
1. updated `englishDictionarySentimentAnalyzer.py` file
   * can conduct Sentiment Analysis by size of the window
1. created `test_englishDictionarySentimentAnalyzer.py` file in `sentimentAnalysis` folder
1. changed the structure of `data` folder
   * created `final` folder to save only the final data
   * created `original` folder to save only the original data
1. edited `mongo_insert.py` file
1. updated *lemmatizer* and *ngram* module in `preprocess` folder

### 0619
1. 0611 version이었으나 업로드 되지 않았던 내용 추가 + 새 graphml output들 공유
1. created 'Cooccurrence' folder
   * created `graphmlmaker.py` to run create graphml files
   * ouput file들 중에서 최종 결과물에 사용된 것은 'graphmls_NVJ' folder에 있는 것들
1. created `test_englishDictionarySentimentAnalyzer.py` file in `preprocess` folder
   * created `cooccurrence` folder to run 'graphmlmaker.py'
   * created `graphml` folder to run 'graphmlmaker.py'
1. changed  '__init__' of `preprocess' folder
   * added lines that import modules above

### 0622
1. updated `englishDictionarySentimentAnalyzer.py` file
   * can filter sentences containing certain keywords
1. updated `test_englishDictionarySentimentAnalyzer.py` file accordingly

### 0623
1. created `englishDictionarySentimentAnalyzer2.py` file (second version)
   * can filter sentences containing certain keywords
1. created `test_englishDictionarySentimentAnalyzer2.py` file (second version)