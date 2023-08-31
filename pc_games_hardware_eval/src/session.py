import datetime
import redis
import random
from component import Component
from system_requirements import GameRequirements


# info_type refers the key name ("user_cpu", "user_gpu" or "user_budget")
def get_user_info_kv(session_id, info_type):
    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 0
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
    key = "session:" + session_id + ":" + info_type
    retrieved_value = redis_client.get(key)
    print("->USER Info", info_type, ":", retrieved_value.decode('ascii'))
    return retrieved_value.decode('ascii')


class UserSession:
    def __init__(self):
        self.redis_host = 'localhost'
        self.redis_port = 6379
        self.redis_db = 0
        self.session_id = None
        self.created_at = None
        self.user_cpu = None
        self.user_gpu = None
        self.user_budget = None
        self.n_searches = 0

    def create_session_kv(self):
        redis_client = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        ct = datetime.datetime.now()
        self.created_at = ct.strftime("%Y-%m-%d %H:%M:%S")
        rand_id = random.randint(0, 1000000)
        self.session_id = str(rand_id)
        key = "session:" + str(self.session_id) + ":created_at"
        # Set the key-value pair in Redis
        redis_client.set(key, self.created_at)
        # Retrieve the value to verify
        retrieved_value = redis_client.get(key)
        print("\n->SESSION (", self.session_id, ") Created at", retrieved_value.decode('ascii'))

    def submit_system_kv(self, cpu_model, gpu_model, budget):
        redis_client = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        self.user_cpu = cpu_model
        self.user_gpu = gpu_model
        self.user_budget = budget
        key = "session:" + str(self.session_id) + ":user_cpu"
        redis_client.set(key, self.user_cpu)
        key = "session:" + str(self.session_id) + ":user_gpu"
        redis_client.set(key, self.user_gpu)
        key = "session:" + str(self.session_id) + ":user_budget"
        redis_client.set(key, self.user_budget)
        print("->USER SYSTEM Submitted")


class Evaluation:
    def __init__(self, session_id, search_number, game_title):
        self.redis_host = 'localhost'
        self.redis_port = 6379
        self.redis_db = 0
        self.session_id = session_id
        self.title = game_title
        self.cpu_result = None
        self.gpu_result = None
        self.search_number = search_number

    def get_system_evaluation(self):
        print("\n->NEW EVALUATION Request")
        redis_client = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        # create components objects
        user_cpu = Component("cpu")
        user_gpu = Component("gpu")
        game_cpu = Component("cpu")
        game_gpu = Component("gpu")
        # read user system info from Key-value DB
        user_cpu_model = get_user_info_kv(self.session_id, "user_cpu")
        user_gpu_model = get_user_info_kv(self.session_id, "user_gpu")
        user_budget_value = float(get_user_info_kv(self.session_id, "user_budget"))
        # find user system benchmarks from Document DB (components collection)
        user_cpu.find_component_by_name(user_cpu_model)
        user_gpu.find_component_by_name(user_gpu_model)
        # find the Game required benchmarks from Document DB (system requirements collection)
        gg = GameRequirements(self.title)
        gg.find_game_requirements()
        game_cpu.find_component_by_id(gg.cpu_id)
        game_gpu.find_component_by_id(gg.gpu_id)
        cpu_result = "true"
        gpu_result = "true"
        if game_cpu.cpu.cpu_mark > user_cpu.cpu.cpu_mark:
            print("\n->EVALUATION: User CPU does NOT meet the Game Requirements!")
            game_cpu.suggest_upgrade(user_cpu.cpu.cpu_mark, user_cpu.category, user_budget_value)
            cpu_result = "false"
        else:
            print("\n->EVALUATION: User CPU is OK for the Game Requirements!")

        if game_gpu.gpu.g3d_mark > user_gpu.gpu.g3d_mark:
            print("\n->EVALUATION: User GPU does NOT meet the Game Requirements!")
            game_gpu.suggest_upgrade(user_gpu.gpu.g3d_mark, user_gpu.category, user_budget_value)
            gpu_result = "false"
        else:
            print("\n->EVALUATION: User GPU is OK for the Game Requirements!")

        key = "session:" + str(self.session_id) + ":evaluation:" + str(self.search_number) + ":" + "title"
        redis_client.set(key, self.title)
        key = "session:" + str(self.session_id) + ":evaluation:" + str(self.search_number) + ":" + "cpu_result"
        redis_client.set(key, cpu_result)
        key = "session:" + str(self.session_id) + ":evaluation:" + str(self.search_number) + ":" + "gpu_result"
        redis_client.set(key, gpu_result)
