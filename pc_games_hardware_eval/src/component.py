import re
from pymongo import MongoClient
import pprint
import uuid


def format_intel_cpu_string(req_cpu):
    """
    Takes an input search string and detects if the Intel CPU naming convention is found
    Return a modified string that improves the queries when searching CPU by name
    :param req_cpu:
    :return: str_fixed
    """
    result = re.search(r'Intel Core [^\s]+', req_cpu)
    if result:
        str_fixed = result.group(0) + " "
        return str_fixed
    result = re.search(r'Core [^\s]+', req_cpu)
    if result:
        str_fixed = result.group(0) + " "
        return str_fixed
    result = re.search(r'Intel Celeron [^\s]+', req_cpu)
    if result:
        str_fixed = result.group(0) + " "
        return str_fixed
    duo_cpu_pattern = re.compile(r' Duo \D\d\d\d\d')
    match2 = duo_cpu_pattern.search(req_cpu)
    quad_cpu_pattern = re.compile(r' Quad \D\d\d\d\d')
    match3 = quad_cpu_pattern.search(req_cpu)
    if match2:
        return match2.group()
    elif match3:
        return match3.group()
    else:
        return req_cpu


def format_category_str(req_category):
    """
    Takes a search string and detects if a "," is present
    To improve the query for a category name, the function returns only the string before the "," char.
    :param req_category:
    :return: parsed_string
    """
    pattern1 = re.compile(r',')
    match1 = pattern1.search(req_category)
    if match1:
        parsed_string = req_category.split(",")[0].strip()
        return parsed_string

    else:
        return req_category


def show_best_cpu_value(category, limit=5, min_score=0):
    """
    Prints the CPUs ordered by Highest CPU Value metric for the specified category.
    Limits the query for a maximum of 100 documents.
    :param category:
    :param limit:
    :param min_score:
    :return:
    """
    print("\n->SHOW Best CPUs (Value Metric), category:", category)
    s_client = MongoClient('mongodb://localhost:27019/?replicaSet=rs0')
    s_db = s_client['project']
    collection = s_db['components']
    if limit > 100:
        print("\n->ERROR: Limit set is to HIGH")
    else:
        pipeline = [
            {
                "$match": {
                    "cpuValue": {"$exists": "true"},
                    "category": {'$regex': category, '$options': 'i'},
                    "cpuMark": {'$gte': min_score},
                }
            },
            {
                "$sort": {
                    "cpuValue": -1
                }
            },
            {
                "$project": {"cpuName": 1, "cpuValue": 1, "price": 1, "cpuMark": 1, "_id": 0}
            },
            {
                "$limit": limit
            },

        ]
        results = collection.aggregate(pipeline)
        for document in results:
            print(document["cpuName"], "- Value:", document["cpuValue"],
                  "CPU Mark:", document["cpuMark"], "Price:", document["price"], "USD")


def show_best_gpu_value(category, limit=5, min_score=0):
    print("\n->SHOW Best GPUs (Value Metric), category:", category)
    s_client = MongoClient('mongodb://localhost:27019/?replicaSet=rs0')
    s_db = s_client['project']
    collection = s_db['components']
    if limit > 100:
        print("Limit set is to HIGH")
    else:
        pipeline = [
            {
                "$match": {
                    "gpuValue": {"$exists": "true"},
                    "category": {'$regex': category, '$options': 'i'},
                    "G3Dmark": {'$gte': min_score},
                }
            },
            {
                "$sort": {
                    "gpuValue": -1
                }
            },
            {
                "$project": {"gpuName": 1, "gpuValue": 1, "price": 1, "G3Dmark": 1, "_id": 0}
            },
            {
                "$limit": limit
            },

        ]
        results = collection.aggregate(pipeline)
        for document in results:
            print(document["gpuName"], "- Value:", document["gpuValue"],
                  "G3D Mark:", document["G3Dmark"], "Price:", document["price"], "USD")


def get_cpu_stats_category(start_year):
    s_client = MongoClient('mongodb://localhost:27019/?replicaSet=rs0')
    s_db = s_client['project']
    collection = s_db['components']
    print("\n->STATISTICS - CPUs statistics per [CATEGORY] from:", start_year)
    # CPUs Distribution per category and core count
    pipeline = [
        {
            "$match": {
                "testDate": {"$gte": start_year}, "cpuMark": {"$exists": "true"}, "price": {"$exists": "true"}
            }
        },
        {
            "$sort": {
                "cpuMark": -1
            }
        },
        {  # group devices by category
            "$group": {
                "_id": "$category",
                "AvgBenchmark": {"$avg": "$cpuMark"},
                "BestName": {"$first": "$cpuName"},
                "BestPerf": {"$first": "$cpuMark"},
                "BestPrice": {"$first": "$price"},
                "AvgPrice": {"$avg": "$price"},
                "Registered": {"$count": {}}
            }
        },
        {
            "$sort": {
                "AvgBenchmark": -1
            }
        },

    ]
    results = collection.aggregate(pipeline)
    if results:
        for document in results:
            # if document["_id"] == "Desktop" or document["_id"] == "Server" or document["_id"] == "Laptop":
            print("\n[", document["_id"], "] Avg. CPU Mark:", round(document["AvgBenchmark"], 2),
                  "; Avg. Price:", round(document["AvgPrice"], 2), "USD ; ",
                  "Number of registered components: ", document["Registered"])
            print("[", document["_id"], "] Best Performance Component:", document["BestName"],
                  "(CPU Mark:", str(document["BestPerf"]), "; Price:", str(document["BestPrice"]), "USD)")
            # pprint.pprint(document)


def get_gpu_stats_category(start_year):
    s_client = MongoClient('mongodb://localhost:27019/?replicaSet=rs0')
    s_db = s_client['project']
    collection = s_db['components']
    print("\n->STATISTICS - GPUs statistics per [CATEGORY] from:", start_year)
    # CPUs Distribution per category and core count
    pipeline = [
        {
            "$match": {
                "testDate": {"$gte": start_year}, "G3Dmark": {"$exists": "true"}, "price": {"$exists": "true"}
            }
        },
        {
            "$sort": {
                "G3Dmark": -1
            }
        },
        {  # group devices by category
            "$group": {
                "_id": "$category",
                "AvgBenchmark": {"$avg": "$G3Dmark"},
                "BestName": {"$first": "$gpuName"},
                "BestPerf": {"$first": "$G3Dmark"},
                "BestPrice": {"$first": "$price"},
                "AvgPrice": {"$avg": "$price"},
                "Registered": {"$count": {}}
            }
        },
        {
            "$sort": {
                "AvgBenchmark": -1
            }
        },

    ]
    results = collection.aggregate(pipeline)
    if results:
        for document in results:
            # if document["_id"] == "Desktop" or document["_id"] == "Server" or document["_id"] == "Laptop":
            print("\n[", document["_id"], "] Avg. G3D Mark:", round(document["AvgBenchmark"], 2),
                  "; Avg. Price:", round(document["AvgPrice"], 2), "USD ; ",
                  "Number of registered components: ", document["Registered"])
            print("[", document["_id"], "] Best Performance Component:", document["BestName"],
                  "(G3D Mark:", str(document["BestPerf"]), "; Price:", str(document["BestPrice"]), "USD)")
            # pprint.pprint(document)


def create_cpu_component(cpu_name, cpu_mark, thread_mark, price, cores, test_date, socket, category):
    component_uuid = str(uuid.uuid4())
    s_client = MongoClient('mongodb://localhost:27019/?replicaSet=rs0')
    s_db = s_client['project']
    collection = s_db['components']
    value = cpu_mark/price
    document = {
        "cpuName": cpu_name,
        "price": price,
        "cpuMark": cpu_mark,
        "cpuValue": value,
        "threadMark": thread_mark,
        "cores": cores,
        "testDate": test_date,
        "socket": socket,
        "category": category,
        "componentID": component_uuid
    }
    result = collection.insert_one(document)
    print(f"\n->CREATE Document CPU Added, mongodbID: {result.inserted_id}")
    print("->COMPONENT ID:", component_uuid)
    return component_uuid


def create_gpu_component(gpu_name, g3d_mark, g2d_mark, price, test_date, category):
    component_uuid = str(uuid.uuid4())
    s_client = MongoClient('mongodb://localhost:27019/?replicaSet=rs0')
    s_db = s_client['project']
    collection = s_db['components']
    gpu_value = g3d_mark/price
    document = {
        "gpuName": gpu_name,
        "G3Dmark": g3d_mark,
        "G2Dmark": g2d_mark,
        "price": price,
        "gpuValue": gpu_value,
        "testDate": test_date,
        "category": category,
        "componentID": component_uuid
    }
    result = collection.insert_one(document)
    print(f"\n->CREATE Document GPU Added, mongodbID: {result.inserted_id}")
    print("->COMPONENT ID:", component_uuid)
    return component_uuid


def update_component(component_uuid, fields):
    s_client = MongoClient('mongodb://localhost:27019/?replicaSet=rs0')
    s_db = s_client['project']
    collection = s_db['components']
    result = collection.update_one(
        {"componentID": component_uuid},
        {"$set": fields}
    )
    if result.matched_count > 0:
        print("\n->UPDATE Component updated successfully")
    else:
        print("\n->UPDATE Component not found")


def delete_component(component_uuid):
    s_client = MongoClient('mongodb://localhost:27019/?replicaSet=rs0')
    s_db = s_client['project']
    collection = s_db['components']
    result = collection.delete_one({"componentID": component_uuid})
    if result.deleted_count > 0:
        print("\n->DELETE Component deleted successfully")
    else:
        print("\n->DELETE Component not found")


class Component:
    def __init__(self, component_type):
        self.client = MongoClient('mongodb://localhost:27019/?replicaSet=rs0')
        self.db = self.client['project']
        self.collection = self.db['components']
        self.mongo_document = None
        self.component_type = component_type
        self.component_id = None
        self.category = None
        self.price = None
        self.test_date = None
        if self.component_type == "cpu":
            self.cpu = self.CpuType()
        elif self.component_type == "gpu":
            self.gpu = self.GpuType()

    class CpuType:
        def __init__(self):
            self.name = None
            self.cpu_mark = None
            self.thread_mark = None
            self.cpu_value = None
            self.socket = None
            self.cores = None

    class GpuType:
        def __init__(self):
            self.name = None
            self.g3d_mark = None
            self.g2d_mark = None
            self.gpu_value = None

    def find_component_by_name(self, component_str):
        if self.component_type == "cpu":
            # check if the component name is AMD Ryzen format
            ryzen = re.search(r'\Dyzen \d [^\s]+', component_str)
            if ryzen:
                component_str = "AMD " + component_str
                re_start = "^"
                re_req_gpu = re_start + component_str + "$"
                cpu_query = {
                    'cpuName': {
                        '$regex': re_req_gpu, '$options': 'i'
                    }
                }
            else:  # try intel component
                f_component_str = component_str + "$"
                cpu_query = {
                    'cpuName': {
                        '$regex': f_component_str, '$options': 'i'
                    }
                }
            query_ret = self.collection.find(cpu_query)
            document_count = self.collection.count_documents(cpu_query)
            if document_count > 1:
                print("\n->NOT FOUND! Find CPU returned multiple components: ")
                for document in query_ret:
                    print(document["cpuName"])
            elif document_count == 0:
                f_component_str = format_intel_cpu_string(component_str)
                cpu_query = {
                    'cpuName': {
                        '$regex': f_component_str, '$options': 'i'
                    }
                }
                query_ret = self.collection.find(cpu_query)
                document_count = self.collection.count_documents(cpu_query)
                if document_count > 1:
                    print("\n->NOT FOUND! Find CPU returned multiple components: ")
                    for document in query_ret:
                        print(document["cpuName"])
                elif document_count == 0:
                    print("\n->NOT FOUND! Find CPU returned zero documents: Component not found/not in database")
                else:
                    print("\n->Find CPU returned: ", document_count)
                    for document in query_ret:
                        print(document["cpuName"])
                        self.mongo_document = document
                        self.parse_cpu_fields_to_object(document)
            else:
                print("\n->Find CPU returned: ", document_count)
                for document in query_ret:
                    print(document["cpuName"])
                    self.mongo_document = document
                    self.parse_cpu_fields_to_object(document)

        elif self.component_type == "gpu":
            re_start = "^"
            re_req_gpu = re_start + component_str + "$"
            gpu_query = {
                'gpuName': {
                    '$regex': re_req_gpu, '$options': 'i'
                }
            }
            query_ret = self.collection.find(gpu_query)
            document_count = self.collection.count_documents(gpu_query)
            if document_count == 0:
                print("\n->Find GPU returned zero documents: Component not found/not in database")
            else:
                print("\n->Find GPU returned: ", document_count)
                for document in query_ret:
                    self.mongo_document = document
                    self.parse_gpu_fields_to_object(document)
                    print(document["gpuName"])

    def find_component_by_id(self, component_uuid_str):
        uuid_query = {
            'componentID': component_uuid_str
        }
        query_ret = self.collection.find(uuid_query)
        document_count = self.collection.count_documents(uuid_query)
        if document_count > 0:
            print("\n->Find UUID returned: ")
            for document in query_ret:
                self.mongo_document = document
                if "cpuName" in document:
                    print(document["cpuName"])
                    self.parse_cpu_fields_to_object(document)
                elif "gpuName" in document:
                    self.parse_gpu_fields_to_object(document)
                    print(document["gpuName"])
        else:
            print("\n->Find UUID returned zero documents")

    # The suggest_upgrade function will provide a search in the available components that
    # have superior performance than this component, constrained by the user budget.
    # This should be used when this component is a minimum requirement for a Game
    # The suggestion will also return the amount of performance increment based on the user component
    def suggest_upgrade(self, user_component_benchmark, user_component_category, user_budget=500):
        user_component_category = format_category_str(user_component_category)
        if self.component_type == "cpu":
            budget_pipeline = [
                {
                    "$match": {
                        "category": {'$regex': user_component_category, '$options': 'i'},
                        "cpuValue": {"$exists": "true"},
                        "price": {"$lte": user_budget}, "cpuMark": {"$gt": self.cpu.cpu_mark}
                    }
                },
                {
                    "$sort": {
                        "cpuValue": -1
                    }
                },
                {
                    "$limit": 2
                },
            ]
            high_perf_pipeline = [
                {
                    "$match": {
                        "category": {'$regex': user_component_category, '$options': 'i'},
                        "cpuValue": {"$exists": "true"},
                        "cpuMark": {"$gt": self.cpu.cpu_mark}
                    }
                },
                {
                    "$sort": {
                        "testDate": -1
                    }
                },
                {
                    "$limit": 1
                },
            ]
            results = self.collection.aggregate(budget_pipeline)
            if results:
                print("\n->CPU Suggestion Found!")
                for document in results:
                    print("$$", document["cpuName"])
                    increment = (100 * (document["cpuMark"] / user_component_benchmark)) - 100
                    increment = round(increment, 1)
                    print("     -Performance increment:", str(increment), "%")
                    print("     -cpuMark:", str(document["cpuMark"]))
                    print("     -Price:", str(document["price"]), "USD")
                    print("     -Category:", str(document["category"]))
            else:
                print("\n->Budget CPU Suggestion Pipeline return zero documents")
            results = self.collection.aggregate(high_perf_pipeline)
            if results:
                print("\n->High Performance CPU Suggestion Found!!")
                for document in results:
                    print("$$$$", document["cpuName"])
                    increment = (100 * (document["cpuMark"] / user_component_benchmark)) - 100
                    increment = round(increment, 1)
                    print("     -Performance increment:", str(increment), "%")
                    print("     -cpuMark:", str(document["cpuMark"]))
                    print("     -Price:", str(document["price"]), "USD")
                    print("     -Category:", str(document["category"]))
            else:
                print("\n->High Perf. Suggestion Pipeline return zero documents")

        elif self.component_type == "gpu":
            budget_pipeline = [
                {
                    "$match": {
                        "category": {'$regex': user_component_category, '$options': 'i'},
                        "gpuValue": {"$exists": "true"},
                        "price": {"$lte": user_budget}, "G3Dmark": {"$gt": self.gpu.g3d_mark}
                    }
                },
                {
                    "$sort": {
                        "cpuValue": -1
                    }
                },
                {
                    "$limit": 2
                },
            ]
            high_perf_pipeline = [
                {
                    "$match": {
                        "category": {'$regex': user_component_category, '$options': 'i'},
                        "gpuValue": {"$exists": "true"},
                        "G3Dmark": {"$gt": self.gpu.g3d_mark}
                    }
                },
                {
                    "$sort": {
                        "testDate": -1
                    }
                },
                {
                    "$limit": 1
                },
            ]
            results = self.collection.aggregate(budget_pipeline)
            if results:
                print("\n->GPU Suggestion Found!")
                for document in results:
                    print("$$", document["gpuName"])
                    increment = (100 * (document["G3Dmark"] / user_component_benchmark)) - 100
                    increment = round(increment, 1)
                    print("     -Performance increment:", str(increment), "%")
                    print("     -G3Dmark:", str(document["G3Dmark"]))
                    print("     -Price:", str(document["price"]), "USD")
                    print("     -Category:", str(document["category"]))
            else:
                print("\n->Budget CPU Suggestion Pipeline return zero documents")
            results = self.collection.aggregate(high_perf_pipeline)
            if results:
                print("\n->High Performance GPU Suggestion Found!!")
                for document in results:
                    print("$$$$", document["gpuName"])
                    increment = (100 * (document["G3Dmark"] / user_component_benchmark)) - 100
                    increment = round(increment, 1)
                    print("     -Performance increment:", str(increment), "%")
                    print("     -G3Dmark:", str(document["G3Dmark"]))
                    print("     -Price:", str(document["price"]), "USD")
                    print("     -Category:", str(document["category"]))
            else:
                print("\n->High Perf. Suggestion Pipeline return zero documents")

    def parse_cpu_fields_to_object(self, document):
        self.component_id = document["componentID"]
        if "category" in document:
            self.category = document["category"]
        if "price" in document:
            self.price = document["price"]
        if "testDate" in document:
            self.test_date = document["testDate"]
        if "cpuName" in document:
            self.cpu.name = document["cpuName"]
        if "cpuMark" in document:
            self.cpu.cpu_mark = document["cpuMark"]
        if "threadMark" in document:
            self.cpu.thread_mark = document["threadMark"]
        if "cpuValue" in document:
            self.cpu.cpu_value = document["cpuValue"]
        if "socket" in document:
            self.cpu.socket = document["socket"]
        if "cores" in document:
            self.cpu.cores = document["cores"]

    def parse_gpu_fields_to_object(self, document):
        self.component_id = document["componentID"]
        if "category" in document:
            self.category = document["category"]
        if "price" in document:
            self.price = document["price"]
        if "testDate" in document:
            self.test_date = document["testDate"]
        if "gpuName" in document:
            self.gpu.name = document["gpuName"]
        if "G3Dmark" in document:
            self.gpu.g3d_mark = document["G3Dmark"]
        if "G2Dmark" in document:
            self.gpu.g2d_mark = document["G2Dmark"]
        if "gpuValue" in document:
            self.gpu.gpu_value = document["gpuValue"]

    def print_component_info(self):
        pprint.pprint(self.mongo_document)

    def create_cpu_component(self, cpu_name, cpu_mark, thread_mark, price, cores, test_date, socket, category):
        component_uuid = str(uuid.uuid4())
        value = cpu_mark/price
        document = {
            "cpuName": cpu_name,
            "price": price,
            "cpuMark": cpu_mark,
            "cpuValue": value,
            "threadMark": thread_mark,
            "cores": cores,
            "testDate": test_date,
            "socket": socket,
            "category": category,
            "componentID": component_uuid
        }
        result = self.collection.insert_one(document)
        print(f"\n->CREATE Document CPU Added, mongodbID: {result.inserted_id}")
        self.parse_cpu_fields_to_object(document)
        self.mongo_document = document

    def create_gpu_component(self, gpu_name, g3d_mark, g2d_mark, price, gpu_value, test_date, category):
        component_uuid = str(uuid.uuid4())
        gpu_value = g3d_mark/price
        document = {
            "gpuName": gpu_name,
            "G3Dmark": g3d_mark,
            "G2Dmark": g2d_mark,
            "price": price,
            "gpuValue": gpu_value,
            "testDate": test_date,
            "category": category,
            "componentID": component_uuid
        }
        result = self.collection.insert_one(document)
        print(f"\n->CREATE Document GPU Added, mongodbID: {result.inserted_id}")
        self.parse_gpu_fields_to_object(document)
        self.mongo_document = document

    def update_component(self, fields):
        result = self.collection.update_one(
            {"componentID": self.component_id},
            {"$set": fields}
        )
        if result.matched_count > 0:
            print("\n->UPDATE Component updated successfully")
        else:
            print("\n->UPDATE Component not found")
        self.find_component_by_id(self.component_id)

    def delete_component(self):
        result = self.collection.delete_one({"componentID": self.component_id})
        if result.deleted_count > 0:
            print("\n->DELETE Component deleted successfully")
        else:
            print("\n->DELETE Component not found")
