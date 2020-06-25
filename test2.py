from mongoengine import *
import datetime
import pymongo as pm
from bson import ObjectId
import os


# pymongo practice
def insert_data(data):
    doc = collection.insert_one(data)
    return doc.inserted_id


connection = pm.MongoClient('localhost', 27017)
database = connection['news_scraping']
collection = database['scraping_result']

print(connection)
print(database)
print(collection)

collection.count_documents()

data = {"name": "Jay"}
insert_data(data)
