import re
from pymongo import MongoClient
import pprint
import uuid



class GameRequirements:
    def __init__(self, title):
        self.client = MongoClient('mongodb://localhost:27019/?replicaSet=rs0')
        self.db = self.client['project']
        self.collection = self.db['system_requirements']
        self.title = title
        self.memory = None
        self.cpu = None
        self.cpu_id = None
        self.gpu = None
        self.gpu_id = None
        self.os_name = None
        self.file_size = None
        self.reviews = None

    def find_game_requirements(self):
        #query = {
        #    'title': {
        #        '$regex': self.title, '$options': 'i'
        #    }
        #}
        query = {
            'title': self.title
        }
        query_ret = self.collection.find(query)
        document_count = self.collection.count_documents(query)
        print("\n->QUERY FOR", self.title, "GAME SYSTEM REQUIREMENTS:")
        if document_count > 0:
            for document in query_ret:
                print("CPU model: ", document["CPU"])
                print("GPU model: ", document["GPU"])
                print("Memory: ", document["Memory"])
                print("File Size: ", document["File Size"])
                self.memory = document["Memory"]
                self.cpu = document["CPU"]
                self.cpu_id = document["CPU_id"]
                self.gpu = document["GPU"]
                self.gpu_id = document["GPU_id"]
                self.os_name = document["OS"]
                self.file_size = document["File Size"]
