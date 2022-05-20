from pymongo import MongoClient


class MongoDb:
    def __init__(self):
        self.client = MongoClient(host='mongodb', port=27017)
        self.db = self.client['burly_pronghorn']
        self.main = self.db['main']

    def insert(self, data):
        """
        Insert one document to mongo Database.

        :param data: validated data dict
        :return: None
        """
        self.main.insert_one(data)

    def find(self, query):
        """
        Find one document in mongo Database.

        :param query: query dict
        :return: all queried objects as list of dictionaries
        """
        return list(self.main.find(query, projection={'_id': False}))

    def delete(self, query):
        """
        Delete one document from mongo Database.

        :param query: query dict
        :return: None
        """
        self.main.delete_one(query)
