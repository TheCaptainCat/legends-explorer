import pymongo


class LegendsConnection:
    def __init__(self, url: str, database: str):
        url = url.replace('[dbname]', database)
        self.client = pymongo.MongoClient(url)
        self.db = self.client[database]
