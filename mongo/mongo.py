import pymongo as pm
from bson import ObjectId
from mongoengine import *
import datetime


# Define embedded documents
# Only used for sentiment analysis
class Sentiment(EmbeddedDocument):
    positive = IntField(min_value=0, max_value=100, default=0)
    negative = IntField(min_value=0, max_value=100, default=0)
    neutral = IntField(min_value=0, max_value=100, default=0)


# Define documents
class Article(DynamicDocument):
    _id = IntField(required=True, primary_key=True)
    date = DateTimeField(required=True)
    content = StringField(required=True)
    source = StringField(required=True, max_length=20)
    country = StringField(default="US")
    category = StringField(default="undefined")
    sentiment = EmbeddedDocumentField(Sentiment)
