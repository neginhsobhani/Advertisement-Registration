from flask_pymongo import pymongo

CONNECTION_STRING = "your_connection_string"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('flask_mongodb_atlas')
collection = pymongo.collection.Collection(db, 'users_collection')


def get_ad_by_id(ad_id):
    mydoc = collection.find_one({'id': ad_id})
    return mydoc


def update_doc_field(ad_id, field, new_value):
    collection.update_one({'id': ad_id}, {"$set": {field: new_value}})


