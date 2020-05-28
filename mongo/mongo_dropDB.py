from mongoengine import *

# Delete news_scraping database
db = connect("news_scraping", host="localhost", port=27017)
db.drop_database("news_scraping")
disconnect()
