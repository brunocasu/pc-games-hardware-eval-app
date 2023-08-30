from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import pprint

MIN_REVIEWS = 500


def show_most_reviewed_games(limit=5):
    print("->SHOW Top", limit, "Most Reviewed Games")
    s_client = MongoClient('mongodb://localhost:27019/?replicaSet=rs0')
    s_db = s_client['project']
    collection = s_db['game_reviews']
    pipeline = [
        {
            "$project": {"new_review": 0}
        },
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
        {
            "$limit": limit
        },
    ]
    results = collection.aggregate(pipeline)
    num_documents = 0
    if results:
        for document in results:
            print(document["_id"], "- Number of Reviews:",document["Registered"])


def show_best_reviewed_games(limit=5):
    print("->SHOW Top", limit, "Best Rated Games")
    s_client = MongoClient('mongodb://localhost:27019/?replicaSet=rs0')
    s_db = s_client['project']
    collection = s_db['game_reviews']
    pipeline = [
        {
            "$group": {
                "_id": "$title",
                "total_reviews": {"$sum": 1},
                "recommended_reviews": {
                    "$sum": {"$cond": [{"$eq": ["$recommendation", "Recommended"]}, 1, 0]}
                }
            }
        },
        {
            "$match": {
                "total_reviews": {'$gte': MIN_REVIEWS},
            }
        },
        {
            "$addFields": {
                "recommended_percentage": {"$multiply": [{"$divide": ["$recommended_reviews", "$total_reviews"]}, 100]}
            }
        },
        {
            "$sort": {"recommended_percentage": -1}
        },
        {
            "$limit": limit
        },
    ]
    results = collection.aggregate(pipeline)
    if results:
        for document in results:
            game_title = document['_id']
            total_reviews = document['total_reviews']
            recommended_reviews = document['recommended_reviews']
            recommended_percentage = document['recommended_percentage']
            print(f"Game: {game_title}")
            print(f"Total Reviews: {total_reviews}")
            print(f"Recommended Reviews: {recommended_reviews}")
            print(f"Percentage of Recommended Reviews: {recommended_percentage:.2f}%")
            print()


def show_latest_reviews(title, limit=5):
    print("->SHOW Latest Reviews of: ", title)
    s_client = MongoClient('mongodb://localhost:27019/?replicaSet=rs0')
    s_db = s_client['project']
    collection = s_db['game_reviews']
    pipeline = [
        {
            "$match": {
                "title": {'$regex': title, '$options': 'i'}
            }
        },
        {
            "$sort": {"date_posted": -1}
        },
        {
            "$limit": limit
        },
    ]
    results = collection.aggregate(pipeline)
    if results:
        for document in results:
            pprint.pprint(document)
            print()


class GameReview:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27019/?replicaSet=rs0')
        self.db = self.client['project']
        self.collection = self.db['game_reviews']
        self.mongo_document = None
        self.title = None
        self.hour_played = None  # int
        self.is_early_access_review = None  # bool
        self.recommendation = None
        self.word_count = None
        self.review = None
        self.date_posted = None
        self.review_id = None  # bson ObjectID saved in string format

    def parse_review_fields_to_object(self, document):
        if "_id" in document:
            self.review_id = str(document["_id"])
        if "hour_played" in document:
            self.hour_played = document["hour_played"]
        if "is_early_access_review" in document:
            self.is_early_access_review = document["is_early_access_review"]
        if "recommendation" in document:
            self.recommendation = document["recommendation"]
        if "title" in document:
            self.title = document["title"]
        if "word_count" in document:
            self.word_count = document["word_count"]
        if "new_review" in document:
            self.review = document["new_review"]
        if "date_posted" in document:
            self.date_posted = document["date_posted"]

    def publish_review(self):
        result = self.collection.insert_one(self.mongo_document)
        print(f"->NEW Review Publish, mongodbID: {result.inserted_id}")
        self.review_id = result.inserted_id

    def delete_review(self):
        result = self.collection.delete_one({"_id": ObjectId(self.review_id)})
        if result.deleted_count > 0:
            print("->DELETED review")
        else:
            print("Review not found")

    def find_review_by_id(self, review_id):
        query_ret = self.collection.find({"_id": ObjectId(review_id)})
        if query_ret:
            print("->SEARCH Found Review:")
            for document in query_ret:
                self.parse_review_fields_to_object(document)
                pprint.pprint(document)
        else:
            print("Review not found")

    def write_review(self, hour_played, is_early_access_review, recommendation, title, new_review):
        date_posted_iso = datetime.utcnow().replace(microsecond=0)
        word_count = len(new_review.split())
        document = {
            "date_posted": date_posted_iso,
            "hour_played": hour_played,
            "is_early_access_review": is_early_access_review,
            "recommendation": recommendation,
            "title": title,
            "word_count": word_count,
            "new_review": new_review
        }
        self.mongo_document = document
        self.parse_review_fields_to_object(document)
        print("\n->REVIEW Submitted:")
        pprint.pprint(self.mongo_document)
        print("->REVIEW Publish?")
