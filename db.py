import pymongo
import urllib
from datetime import datetime
from bson.objectid import ObjectId

class DynamoDB:

    def __init__(self):
        self.db = 'search-engine-db'
        self.table = 'search-engine-collection'
        self.username = 'navinbalaji1996_db_user'
        self.password = 'XUuBLBEMjLCbZqHq'
        self.connect_db()

    def connect_db(self):
        self.cluster = pymongo.MongoClient(f"mongodb+srv://{self.username}:"+ urllib.parse.quote(self.password)
                          + "@search-engine-cluster.zk6k2bd.mongodb.net/?retryWrites=true&w=majority&appName=search-engine-cluster")
        
    def close_db(self):
        self.cluster.close()

    def put_object(self, query, response):
        db_instance = self.cluster[self.db]
        table_instance = db_instance[self.table]
        doc = {'query': query, 'response': response}
        table_instance.insert_one(doc)
        return 'Object is updated'
    
    def get_object(self, name):
        db_instance = self.cluster[self.db]
        table_instance = db_instance[self.table]
        objects = list(table_instance.find({"name": {"$regex": name, "$options": "i"}}))
        return objects
    
    def get_object_by_name(self, name):
        db_instance = self.cluster[self.db]
        table_instance = db_instance[self.table]
        objects = list(table_instance.find({"name": {"$regex": name, "$options": "i"}}))
        unique_names = {each['name'] for each in objects}
        return list(unique_names)
    
    def delete_object(self, id):
        db_instance = self.cluster[self.db]
        table_instance = db_instance[self.table]
        table_instance.delete_one({"_id": ObjectId(id)})

if __name__ == '__main__':
    db = DynamoDB()
