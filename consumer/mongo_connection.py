from pymongo import MongoClient
import os


class MongoConnection:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGO_URI", "mongodb://admin:secretpass@localhost:27017")
        self.mongo_db = os.getenv("MONGO_DB", "alerts_db")
        self.client = None

    def check_mongo_connection(self):
        if self.client:
            self.client.admin.command('ping')

    def get_client(self):
        if self.client:
            try:
                self.check_mongo_connection()
                return self.client
            except Exception as e:
                raise ConnectionError(f"Failed to connect to the 'old' mongo connection {self.mongo_uri}: {str(e)}")
        try:
            self.client = MongoClient(self.mongo_uri)
            self.check_mongo_connection()
            return self.client
        except Exception as e:
            raise ConnectionError(f"Failed to connect to the 'new' mongo connection{self.mongo_uri}: {str(e)}")

    def get_db(self):
        client = self.get_client()
        return client[self.mongo_db]

    def get_collection(self):
        db = self.get_db()
        return db[os.getenv("MONGO_COLLECTION", "alerts")]

    def insert_alert(self, alert):
        collection = self.get_collection()
        collection.insert_one(alert)
