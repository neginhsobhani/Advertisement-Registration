from flask_pymongo import pymongo

CONNECTION_STRING = "your_connection_string"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('flask_mongodb_atlas')
collection = pymongo.collection.Collection(db, 'users_collection')


def generate_new_id():
    new_ad_id = collection.count_documents({}) + 1
    return new_ad_id


def get_ad_by_id(ad_id):
    mydoc = collection.find_one({'id': ad_id})
    return mydoc


def insert_new_ad(id, email, description, url):
    new_ad = {"id": id, "email": email, "description":
              description, "state": "processing", "category": "none", "url": url}
    collection.insert_one(new_ad)
