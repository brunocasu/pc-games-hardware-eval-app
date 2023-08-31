from pymongo import MongoClient
from component import Component


def create_system_requirement(title, memory, cpu_model, gpu_model, os_name, file_size):
    print(f"\n->CREATE System Requirements for:", title)
    s_client = MongoClient('mongodb://localhost:27019/?replicaSet=rs0')
    s_db = s_client['project']
    collection = s_db['system_requirements']
    # find CPU_id
    cpu_obj = Component("cpu")
    cpu_obj.find_component_by_name(cpu_model)
    # find GPU_id
    gpu_obj = Component("gpu")
    gpu_obj.find_component_by_name(gpu_model)
    document = {
        "Memory": memory,
        "GPU": cpu_model,
        "CPU": gpu_model,
        "File Size": file_size,
        "OS": os_name,
        "title": title,
        "CPU_id": cpu_obj.component_id,
        "GPU_id": gpu_obj.component_id
    }
    result = collection.insert_one(document)
    print(f"Game mongodbID: {result.inserted_id}")
    return title


def update_system_requirement(game_title, fields):
    s_client = MongoClient('mongodb://localhost:27019/?replicaSet=rs0')
    s_db = s_client['project']
    collection = s_db['system_requirements']
    result = collection.update_one(
        {"title": game_title},
        {"$set": fields}
    )
    if result.matched_count > 0:
        print("\n->UPDATE System Requirement updated successfully")
    else:
        print("\n->UPDATE System Requirement not found")


def delete_system_requirement(game_title):
    s_client = MongoClient('mongodb://localhost:27019/?replicaSet=rs0')
    s_db = s_client['project']
    collection = s_db['system_requirements']
    result = collection.delete_one({"title": game_title})
    if result.deleted_count > 0:
        print("\n->DELETE System Requirement deleted successfully")
    else:
        print("\n->DELETE System Requirement not found")


def update_embedded_reviews(game_title):
    s_client = MongoClient('mongodb://localhost:27019/?replicaSet=rs0')
    s_db = s_client['project']
    collection = s_db['system_requirements']
    # get the current system requirements document
    query = {
        'title': game_title
    }
    query_ret = collection.find(query)
    document_count = collection.count_documents(query)
    print("\n->UPDATE REVIEWS FOR", game_title, "IN GAME SYSTEM REQUIREMENTS")
    game_document = []
    if document_count > 0:
        for document in query_ret:
            game_document = document
            # print(game_document)
    # fetch last 20 reviews
    collection = s_db['game_reviews']
    pipeline = [
        {
            "$match": {
                "title": {'$regex': game_title, '$options': 'i'}
            }
        },
        {
            "$sort": {"date_posted": -1}
        },
        {
            "$limit": 20
        },
    ]
    results = collection.aggregate(pipeline)
    embedded_reviews = []
    if results:
        for document in results:
            embedded_reviews.append(document)
            # print(embedded_reviews)
    game_document["reviews"] = embedded_reviews
    # print(game_document)
    collection = s_db['system_requirements']
    result = collection.update_one(
        {"title": game_title},
        {"$set": game_document}
    )
    if result.matched_count > 0:
        print("\n->UPDATE Reviews successfully")
    else:
        print("\n->UPDATE Reviews failed")


def show_embedded_reviews(game_title):
    gg = GameRequirements(game_title)
    gg.find_game_requirements()
    print("\n->SHOW THE LATEST REVIEWS FOR: ", game_title)
    for document in gg.reviews:
        print(document)


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
                if "reviews" in document:
                    self.reviews = document["reviews"]



