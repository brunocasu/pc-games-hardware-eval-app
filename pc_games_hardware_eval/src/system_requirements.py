

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
