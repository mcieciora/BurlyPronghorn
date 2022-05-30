from pymongo import MongoClient


class MongoDb:
    def __init__(self):
        self.client = MongoClient(host='mongodb', port=27017)
        self.db = self.client['burly_pronghorn']
        self.main = self.db['main']
        self.users = self.db['users']

    def insert(self, data):
        return_value = True
        query = {'object_name': data['object_name']}
        if len(list(self.main.find(query))) == 0:
            self.main.insert_one(data)
        else:
            return_value = False
        return return_value

    def insert_user(self, data):
        return_value = True
        query = {'username': data['username']}
        if len(list(self.users.find(query))) == 0:
            self.users.insert_one(data)
        else:
            return_value = False
        return return_value

    def find(self, query):
        return list(self.main.find(query, projection={'_id': False}))

    def delete(self, query):
        if len(list(self.main.find(query))) == 0:
            return False
        else:
            self.main.delete_one(query)
            return True
