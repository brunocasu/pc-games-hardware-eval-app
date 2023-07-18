import csv
import json
import uuid
import re
import pandas as pd
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['local']

csv_delimiter = ","  # Specify the delimiter used in your CSV file
csv_encoding = "utf-8"  # Specify the encoding used in your CSV file


def convert_csv_to_json(csv_file_path, json_file_path):
    with open(csv_file_path, "r", encoding=csv_encoding) as file:
        csv_data = csv.DictReader(file, delimiter=csv_delimiter)

        # Convert CSV data to a list of dictionaries
        data = [row for row in csv_data]

        # Write the data to a JSON file
    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=4)


def add_uuid(json_file_path, csv_file_path):
    # Read the JSON file
    with open(json_file_path, "r") as file:
        data = json.load(file)
    # Iterate through each document
    for document in data:
        # Generate a new UUID for "componentID"
        document["componentID"] = str(uuid.uuid4())
    # Write the updated data back to the JSON file
    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=4)

    # Read the JSON file
    with open(json_file_path, "r") as file:
        data = json.load(file)

    # Convert JSON data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Write the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)


def fix_system_requirements_cpu_string(req_cpu):
    # two_cpu_pattern = re.compile(r' or ')
    # match1 = two_cpu_pattern.search(req_cpu)
    result = re.search(r'Intel Core [^\s]+', req_cpu)
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


def fix_system_requirements_gpu_string(req_gpu):
    pattern1 = re.compile(r'  or ')
    match1 = pattern1.search(req_gpu)
    if match1:
        parsed_string = req_gpu.split("  or")[0].strip()
        return parsed_string

    else:
        return req_gpu


def add_uuid_in_system_req(req_json_file_path):
    # Read the JSON file
    with open(req_json_file_path, "r") as file:
        req_data = json.load(file)
    nomatch_cpu = 0
    match2_cpu = 0
    nomatch_gpu = 0
    match2_gpu = 0
    collection = db['components']

    # Iterate through each document in the system requirements dataset
    for req_document in req_data:
        req_cpu = req_document["CPU"]
        req_gpu = req_document["GPU"]
        # exclude similar components
        req_cpu = fix_system_requirements_cpu_string(req_cpu)
        req_gpu = fix_system_requirements_gpu_string(req_gpu)
        collection = db['components']

        cpu_query = {
            'cpuName': {
                '$regex': req_cpu, '$options': 'i'
            }
        }
        cpu_projection = {"componentID": 1, "_id": 0}
        query_ret = collection.find(cpu_query,cpu_projection)
        document_count = collection.count_documents(cpu_query)
        if document_count > 1:
            match2_cpu = match2_cpu + 1
        elif document_count == 0:
            #print("----CPU NOT FOUND",req_cpu)
            req_document["CPU_id"] = ""
            nomatch_cpu = nomatch_cpu + 1

        if query_ret:
            for doc in query_ret:
                uuid_rec_bin = doc["componentID"]
                string_uuid = str(uuid.UUID(bytes=uuid_rec_bin))
                req_document["CPU_id"] = string_uuid
                break

        ## GPU query
        re_start = "^"
        re_req_gpu = re_start + req_gpu + "$"
        gpu_query = {
            'gpuName': {
                '$regex': re_req_gpu, '$options': 'i'
            }
        }
        gpu_projection = {"componentID": 1, "_id": 0}
        query_ret = collection.find(gpu_query,gpu_projection)
        document_count = collection.count_documents(gpu_query)
        if document_count == 1:
            if query_ret:
                for doc in query_ret:
                    uuid_rec_bin = doc["componentID"]
                    string_uuid = str(uuid.UUID(bytes=uuid_rec_bin))
                    req_document["GPU_id"] = string_uuid
                    break
        elif document_count == 0:
            # not found in specific search
            gpu_query = {
                'gpuName': {
                    '$regex': req_gpu, '$options': 'i'
                }
            }
            gpu_projection = {"componentID": 1, "_id": 0}
            query_ret = collection.find(gpu_query,gpu_projection)
            document_count = collection.count_documents(gpu_query)
            if document_count > 1:
                match2_gpu = match2_gpu + 1
                #print("DUPLICATE GPU FOUND", req_gpu)
                if query_ret:
                    for doc in query_ret:
                        uuid_rec_bin = doc["componentID"]
                        string_uuid = str(uuid.UUID(bytes=uuid_rec_bin))
                        req_document["GPU_id"] = string_uuid
                        break
            elif document_count == 0:
                #print("GPU NOT FOUND", req_gpu)
                req_document["GPU_id"] = ""
                nomatch_gpu = nomatch_gpu + 1
            else:
                if query_ret:
                    for doc in query_ret:
                        uuid_rec_bin = doc["componentID"]
                        string_uuid = str(uuid.UUID(bytes=uuid_rec_bin))
                        req_document["GPU_id"] = string_uuid
                        break


    # Write the updated data back to the JSON file
    with open(req_json_file_path, "w") as file:
        json.dump(req_data, file, indent=4)
    print("Add UUID End ")
    print("Games with no CPU in the dataset: " + str(nomatch_cpu))
    print("Games with 2 or more CPU in the dataset: " + str(match2_cpu))
    print("Games with no GPU in the dataset: " + str(nomatch_gpu))
    print("Games with 2 or more GPU in the dataset: " + str(match2_gpu))


#csv_path = "CPU_benchmark_v4.csv"  # Replace with the actual path to your CSV file
#cpu_json_path = "cpu_bm.json"  # Replace with the desired path for the JSON file
#convert_csv_to_json(csv_path, cpu_json_path)
#add_uuid(cpu_json_path, "cpu_bm_uuid.csv")

#csv_path = "GPU_benchmarks_v7.csv"  # Replace with the actual path to your CSV file
#gpu_json_file_path = "gpu_bm.json"  # Replace with the desired path for the JSON file
#convert_csv_to_json(csv_path, gpu_json_file_path)
#add_uuid(gpu_json_file_path, "gpu_bm_uuid.csv")

#result = re.search(r'Intel Core [^\s]+', 'Intel Core i5-5400F or XXX')
#print ("RESULT", result.group(0))


csv_path = "system_req_uuid.csv"  # Replace with the actual path to your CSV file
req_json_path = "system_req_uuid.json"  # Replace with the desired path for the JSON file
#convert_csv_to_json(csv_path, req_json_path)
#add_uuid_in_system_req(req_json_path)
# Read the JSON file
with open(req_json_path, "r") as file:
    data = json.load(file)

# Convert JSON data to a pandas DataFrame
df = pd.DataFrame(data)

# Write the DataFrame to a CSV file
df.to_csv(csv_path, index=False)

