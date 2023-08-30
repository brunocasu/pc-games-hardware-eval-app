from component import Component
from component import get_gpu_stats_category, \
    get_cpu_stats_category, show_best_cpu_value, show_best_gpu_value
from game_review import GameReview
from game_review import show_most_reviewed_games, show_best_reviewed_games, show_latest_reviews
import uuid
from bson import Binary, UuidRepresentation


# PC Components (Evaluation Functions)
# Users: 5.	View a selected Component benchmarks and price.
def search_component(component_type, model):
    search_component = Component(component_type)
    search_component.find_component_by_name(model)
    search_component.print_component_info()


# Users: 6.	View the Components with the highest value metric.
def show_best_value_components(component_type, category, limit_p=5, min_benchmark=0):
    if component_type == "cpu":
        show_best_cpu_value(category, limit_p, min_benchmark)
    elif component_type == "gpu":
        show_best_gpu_value(category, limit_p, min_benchmark)


# Users: 7.	Submit its own System Configuration. TODO
def submit_my_system(cpu_name, gpu_name, session_id):
    print("a")

# Users: 9.	Update its submitted System Configuration. TODO


# Users: 10.	Obtain a System Evaluation TODO


# Users: 11.	Obtain a suggestion for a System Upgrade, based on a selected PC game.
# Managers: 2.	Create/update/delete a component information.

# Reviews and PC games requirements (Browsing Functions)
# Users: 1.	View most reviewed PC games.
# Users: 2.	View best reviewed PC games.
# Users: 3.	View latest reviews of a selected PC game.
# Users: 4.	View the System Requirements for a selected PC game.
# Users: 8.	Submit a simple review of a PC game.
# Managers: 1.	Create/update/delete a PC game information.
# Managers: 3.	Delete a PC game review.

# Statistics (Additional Functions)
# Managers: 4.	View statistics for Components, based on the categories.
# Managers: 5.	View statistics for PC game reviews.
# Managers: 6.	View all PC game reviews.


#user_cpu = Component("cpu")
#user_gpu = Component("gpu")

# game_cpu = Component("cpu")
#game_gpu = Component("gpu")

#user_cpu.find_component_by_id("7c1ee222-7b64-4b5e-b338-c4fd325e8449")
# user_cpu.print_component_info()
# game_cpu.find_component_by_name("Ryzen 7 5700U")

#user_gpu.find_component_by_name("geforce gtx 950")
#game_gpu.find_component_by_name("Geforce gtx 1050 Ti")

# if game_cpu.cpu.cpu_mark > user_cpu.cpu.cpu_mark:
# print("->User CPU does NOT meet the Game Requirements!")
# game_cpu.suggest_upgrade(user_cpu.cpu.cpu_mark, user_cpu.category, 500)

#if game_gpu.gpu.g3d_mark > user_gpu.gpu.g3d_mark:
    #print("->User GPU does NOT meet the Game Requirements!")
    #game_gpu.suggest_upgrade(user_gpu.gpu.g3d_mark, user_gpu.category, 500)

# get_cpu_stats_category(2020)
# get_gpu_stats_category(2015)
# show_best_cpu_value("Desktop", min_score=5000)
# show_best_gpu_value("Desktop", 2)

# new_cpu = Component("cpu")
# new_cpu.create_cpu_component("AMD Ryzen Threadripper 5995WX", 100000, 3330, 64, 2023, "sWRX8", "Desktop")
# new_cpu.find_component_by_id("new_cpu.component_id")
# new_cpu.print_component_info()

# new_gpu = Component("gpu")
# new_gpu.create_gpu_component("GeForce RTX 3190 Ti", 29000, 1117, 2099.99, 13.85, 2023, "Desktop")
# new_gpu.print_component_info()

# new_cpu.update_component({"category": "Server"})
# new_gpu.update_component({"category": "AAAAAAAA"})
# new_cpu.delete_component()
# new_gpu.delete_component()

# show_most_reviewed_games(limit=50)
# show_best_reviewed_games()

# game_review = GameReview()
# game_review.write_review(1000, "false", "Recommended", "Dead by Daylight", "kkkkkkkkk kkk kkkkk")
# print(game_review.review_id)
# game_review.publish_review()
# show_latest_reviews("Dead by Daylight")


# show_latest_reviews("Dead by Daylight")
# search_review = GameReview()
# search_review.find_review_by_id(game_review.review_id)
# search_review.delete_review()
# show_latest_reviews("Dead by Daylight")

## !! Need Redis
def connect_to_app():
    print("->CONNECT To application...")
    # return session ID
    # return random integer
    # generate session number



## OK Mongo !! Need Redis
def user_submit_my_system(cpu_name, gpu_name):
    print("->USER Submitted components")
    print("->USER CPU Found in database!")
    print("->USER GPU Found in database!")
    # REDIS: write session/1111/user/cpu: component_id
    # REDIS: write session/1111/user/gpu: component_id


## OK
def show_best_reviewed_games(limit):
    print("->SHOW Games with the highest Recommendation percentage")


## OK
def show_most_reviewed_games(limit):
    print("->SHOW Games with the highest Number of reviews")


## OK
def show_latest_reviews(game_name, limit):
    print("->SHOW Latest reviews from: ", game_name)



## Mongo Need Class !! Need Redis
def search_game(game_name):
    print("->SEARCH Game Found in database!")
    # REDIS: read session/1111/user/cpu:
    # REDIS: read session/1111/user/gpu:
    # REDIS: read session/1111/user/game_searches:
    # REDIS: write session/1111/user/game_searches: +1

    # if component_id:
    # REDIS: write session/1111/game_eval/1/title: string
    # REDIS: write session/1111/game_eval/1/cpu: bool
    # REDIS: write session/1111/game_eval/1/gpu: bool


## OK
def post_review(hour_played, recommendation, title, new_review):
    print("->SEARCH Component Found in database!")
