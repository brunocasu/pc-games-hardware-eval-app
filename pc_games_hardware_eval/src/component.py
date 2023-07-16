import re
from pymongo import MongoClient
import pprint

client = MongoClient('mongodb://localhost:27017/')
db = client['local']


def format_intel_cpu_string(req_cpu):
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


class Component:
    def __init__(self, component_type):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = client['local']
        self.collection = db['components']
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
            else: # try intel component
                f_component_str = component_str + "$"
                cpu_query = {
                    'cpuName': {
                        '$regex': f_component_str, '$options': 'i'
                    }
                }
            query_ret = self.collection.find(cpu_query)
            document_count = self.collection.count_documents(cpu_query)
            if document_count > 1:
                print("->NOT FOUND! Find CPU returned multiple components: ")
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
                    print("->NOT FOUND! Find CPU returned multiple components: ")
                    for document in query_ret:
                        print(document["cpuName"])
                elif document_count == 0:
                    print("->NOT FOUND! Find CPU returned zero documents: Component not found/not in database")
                else:
                    print("->Find CPU returned: ")
                    for document in query_ret:
                        print(document["cpuName"])
                        self.mongo_document = document
                        self.parse_cpu_fields_to_object(document)
            else:
                print("->Find CPU returned: ")
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
                print("->Find GPU returned zero documents: Component not found/not in database")
            else:
                print("->Find GPU returned: ")
                for document in query_ret:
                    print(document["gpuName"])

    def find_component_by_id(self, component_uuid_str):
        uuid_query = {
            'componentID': component_uuid_str
        }
        query_ret = self.collection.find(uuid_query)
        document_count = self.collection.count_documents(uuid_query)
        if document_count > 0:
            print("->Find UUID returned: ")
            for document in query_ret:
                if "cpuName" in document:
                    print(document["cpuName"])
                    self.parse_cpu_fields_to_object(self, document)
                elif "gpuName" in document:
                    self.parse_gpu_fields_to_object(self, document)
                    print(document["gpuName"])
        else:
            print("->Find UUID returned zero documents")

    # The suggest_upgrade function will provide a search in the available components that
    # have superior performance than this component, constrained by the user budget.
    # This should be used when this component is a minimum requirement for a Game
    # The suggestion will also return the amount of performance increment based on the user component
    def suggest_upgrade(self, user_component_benchmark, user_component_category, user_budget):
        if self.component_type == "cpu":
            print("->Init Budget Pipeline")
            budget_pipeline = [
                {
                    "$match": {
                        "category": {'$regex': user_component_category, '$options': 'i'}, "cpuValue": {"$exists": "true"},
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
                        "category": {'$regex': user_component_category, '$options': 'i'}, "cpuValue": {"$exists": "true"},
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
                print("->Budget Component Suggestion Found:")
                for document in results:
                    print(document["cpuName"])
                    increment = (100*(document["cpuMark"]/user_component_benchmark)) - 100
                    increment = round(increment,1)
                    print("  -Performance increment:", str(increment), "%")
                    print("  -Price:", str(document["price"]), "USD")
            else:
                print("->Budget Suggestion Pipeline return zero documents")
            results = self.collection.aggregate(high_perf_pipeline)
            if results:
                print("->High Performance Suggestion Found:")
                for document in results:
                    print(document["cpuName"])
                    increment = (100*(document["cpuMark"]/user_component_benchmark)) - 100
                    increment = round(increment,1)
                    print("  -Performance increment:", str(increment), "%")
                    print("  -Price:", str(document["price"]), "USD")
            else:
                print("->Budget Suggestion Pipeline return zero documents")

        elif self.component_type == "gpu":
            print("->Find UUID returned zero documents")

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