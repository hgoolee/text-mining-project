# -*- encoding:utf8 -*-
import preprocess as pre
from controlDB import *
from mongoengine import *
import datetime
from preprocessByDate import process_by_date
from preprocessByCategory import process_by_category
from preprocessBySource import process_by_source
from wordcloud_generate import generate_wordcloud

# TODO: Choose a filter to execute
# mode is 1 -- filter by date
# mode is 2 -- filter by category
# mode is 3 -- filter by source
mode = 3

# TODO: Select whether to generate Word Cloud
# True -- Generate Word Cloud
# False -- Do not generate Word Cloud
generateWordCloud = False

if mode == 1:
    # TODO: Choose a range of dates to extract news articles
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

elif mode == 2:
    # TODO: Choose categories to extract news articles
    categoryArray = ["mask"]

    for category in categoryArray:
        doc_collection = process_by_category(category)
        if generateWordCloud:
            generate_wordcloud(doc_collection)

elif mode == 3:
    # TODO: Choose sources to extract news articles
    sourceArray = ["Chicago Tribune"]

    for source in sourceArray:
        doc_collection = process_by_source(source)
        if generateWordCloud:
            generate_wordcloud(doc_collection)

else:
    print("Mode is not defined!")
