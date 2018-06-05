from pymongo import MongoClient

class MongodbOperator:
    def __init__(self, mongodb_addr, mongodb_port, mongodb_username, mongodb_passwd, mongodb_Database, mongodb_collection):
        self.client = MongoClient(mongodb_addr, mongodb_port)
        self.db = self.client[mongodb_Database]
        self.db.authenticate(mongodb_username, mongodb_passwd)
        self.collection = self.db[mongodb_collection]

    def insert_db(self, item, collection_name=None):
        if collection_name !=None:
            collection = self.db.get_collection(self.db)
            collection.insert(item)
        else:
            self.collection.insert(item)

    def find_db(self, expression=None, collection_name=None):
        if collection_name != None:
            collection=self.db.get_collection(self.db)
            if expression !=None:
                return collection.find(expression)
            else:
                return collection.find()
        else:
            if expression != None:
                return self.collection.find(expression)
            else:
                return self.collection.find()


if __name__ == '__main__':
    mongodb_addr = '139.219.64.238'
    mongodb_port = 27017
    mongodb_username = 'c004517c-2d95-498c-a5c7-900f22620314'
    mongodb_passwd = 'EvoPzLheHf10iudSDag83WbSi'
    mongodb_Database = '1cdc85b4-8fda-4361-be1c-9ccb588ddd5e'
    mongodb_collection = 'common_Modbus_Handler'

    test = MongodbOperator(mongodb_addr, mongodb_port, mongodb_username, mongodb_passwd, mongodb_Database,
                           mongodb_collection)
    print(test.find_db())