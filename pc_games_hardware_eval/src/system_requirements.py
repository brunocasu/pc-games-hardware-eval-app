import re
from pymongo import MongoClient
import pprint
import uuid

def update_all_latest_reviews():
    s_client = MongoClient('mongodb://localhost:27017/')
    s_db = s_client['local']
    collection = s_db['game_reviews']
    # find all games with reviews
    pipeline1 = [
        {
            "$group": {
                "_id": "$title",
                "Registered": {"$count": {}}
            }
        },
        {
            "$sort": {
                "Registered": -1
            }
        },
    ]
    results = collection.aggregate(pipeline1)
    if results:
        # for every game found, get latest reviews
        for document in results:
            print(document["_id"])
            max_embedded_reviews = 20

            pipeline2 = [
                {
                    "$match": {
                        "title": {'$regex': document["_id"], '$options': 'i'}
                    }
                },
                {
                    "$sort": {"date_posted": -1}
                },
                {
                    "$limit": max_embedded_reviews
                },
            ]
            #reviews = collection.aggregate(pipeline2)
            for
            collection = s_db['system_requirements']
            result = collection.update_one(
                {"componentID": component_uuid},
                {"$set": fields}
            )
            if result.matched_count > 0:
                print("->UPDATED REVIEWS for: ", document["_id"])
            else:
                print("->UPDATE Component not found")


    for game_name in list_of_games:
        game_query = {
            'title': {
                '$regex': game_name, '$options': 'i'
            }
        }
        collection = s_db['system_requirements']
        query_ret = collection.find(game_query)
        if query_ret:
            for document in query_ret:
                num_documents = num_documents + 1
                print(document["title"], document["Memory"])
    print("->Number of Games From System Requirements:", num_documents)



class GameRequirements:
    def __init__(self):
        self.title = None
        self.memory = None
        self.cpu = None
        self.cpu_id = None
        self.gpu = None
        self.gpu_id = None
