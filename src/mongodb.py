from pymongo import MongoClient


class MongoDb:
    def __init__(self):
        self.client = MongoClient(host='mongodb', port=27017)
        self.db = self.client['burly_pronghorn']
        self.main = self.db['main']

    def insert(self, data):
        pass

    def find(self, query):
        pass

    def delete(self, query):
        pass
