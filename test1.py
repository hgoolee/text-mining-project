# -*- encoding:utf8 -*-
import preprocess as pre
from controlDB import *
from mongoengine import *
import datetime
from preprocessByDateRange import process_by_date_range
from preprocessByDate import process_by_date
from preprocessByCategory import process_by_category
from preprocessBySource import process_by_source
from preprocessByKeyword import process_by_keyword
from wordcloud_generate import generate_wordcloud

# TODO: Choose a filter to execute
# mode is 1 -- filter by date range (whole period)
# mode is 2 -- filter by date (each date)
# mode is 3 -- filter by category
# mode is 4 -- filter by source
# mode is 5 -- filter by keyword (case insensitive)
mode = 5

# TODO: Select whether to generate Word Cloud
# True -- Generate Word Cloud
# False -- Do not generate Word Cloud
generateWordCloud = False

if mode == 1:
    # TODO: Choose a range of dates to extract news articles
    #  Output TWO files - 1) articles of the whole period  2) pre-processed result of the whole period
    #  Extract every article from startYear/startMonth/startDay to endYear/endMonth/endDay
    startYear = "2020"
    startMonth = "04"
    startDay = "15"

    endYear = "2020"
    endMonth = "05"
    endDay = "15"

    start_date = datetime.datetime(int(startYear), int(startMonth), int(startDay))
    end_date = datetime.datetime(int(endYear), int(endMonth), int(endDay))

    doc_collection = process_by_date_range(start_date, end_date)
    if generateWordCloud:
        generate_wordcloud(doc_collection)

elif mode == 2:
    # TODO: Choose a range of dates to extract news articles
    #  Output MULTIPLE files - Each file consists of pre-processed result of each date
    #  Extract every article from startYear/startMonth/startDay to endYear/endMonth/endDay
    startYear = "2020"
    startMonth = "05"
    startDay = "13"

    endYear = "2020"
    endMonth = "05"
    endDay = "15"

    start_date = datetime.datetime(int(startYear), int(startMonth), int(startDay))
    end_date = datetime.datetime(int(endYear), int(endMonth), int(endDay))
    one_day = datetime.timedelta(days=1)

    current_date = start_date
    while current_date <= end_date:
        doc_collection = process_by_date(str(current_date.year), str(current_date.month).zfill(2), str(current_date.day).zfill(2))
        if generateWordCloud:
            generate_wordcloud(doc_collection)
        current_date += one_day

elif mode == 3:
    # TODO: Choose categories to extract news articles
    categoryArray = ["mask"]

    for category in categoryArray:
        doc_collection = process_by_category(category)
        if generateWordCloud:
            generate_wordcloud(doc_collection)

elif mode == 4:
    # TODO: Choose sources to extract news articles
    sourceArray = ["Chicago Tribune"]

    for source in sourceArray:
        doc_collection = process_by_source(source)
        if generateWordCloud:
            generate_wordcloud(doc_collection)

elif mode == 5:
    # TODO: Choose keywords (case insensitive) to extract news articles
    keywordArray = ["South Korea", "mask"]

    for keyword in keywordArray:
        doc_collection = process_by_keyword(keyword)
        if generateWordCloud:
            generate_wordcloud(doc_collection)

else:
    print("Mode is not defined!")
