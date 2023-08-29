from component import Component
from component import get_gpu_stats_category, \
    get_cpu_stats_category, show_best_cpu_value, show_best_gpu_value
from game_review import GameReview
from game_review import show_most_reviewed_games, show_best_reviewed_games, show_latest_reviews
import uuid
from bson import Binary, UuidRepresentation

#user_cpu = Component("cpu")
#user_gpu = Component("gpu")

#game_cpu = Component("cpu")
#game_gpu = Component("gpu")

#user_cpu.find_component_by_name("Core i5-9400F")
#user_cpu.print_component_info()
#game_cpu.find_component_by_name("Ryzen 7 5700U")

#user_gpu.find_component_by_name("geforce gtx 950")
#game_gpu.find_component_by_name("Geforce gtx 1050 Ti")

#if game_cpu.cpu.cpu_mark > user_cpu.cpu.cpu_mark:
    #print("->User CPU does NOT meet the Game Requirements!")
    #game_cpu.suggest_upgrade(user_cpu.cpu.cpu_mark, user_cpu.category, 500)

#if game_gpu.gpu.g3d_mark > user_gpu.gpu.g3d_mark:
    #print("->User GPU does NOT meet the Game Requirements!")
    #game_gpu.suggest_upgrade(user_gpu.gpu.g3d_mark, user_gpu.category, 230)

#get_cpu_stats_category(2020)
#get_gpu_stats_category(2015)
show_best_cpu_value("Desktop", min_score=5000)
#show_best_gpu_value(2, "Desktop")

#new_cpu = Component("cpu")
#new_cpu.create_cpu_component("AMD Ryzen Threadripper 5995WX", 100000, 3330, 64, 2023, "sWRX8", "Desktop")
#new_cpu.find_component_by_id("new_cpu.component_id")
#new_cpu.print_component_info()

#new_gpu = Component("gpu")
#new_gpu.create_gpu_component("GeForce RTX 3190 Ti", 29000, 1117, 2099.99, 13.85, 2023, "Desktop")
#new_gpu.print_component_info()

#new_cpu.update_component({"category": "Server"})
#new_gpu.update_component({"category": "AAAAAAAA"})
#new_cpu.delete_component()
#new_gpu.delete_component()

#show_most_reviewed_games(limit=50)
#show_best_reviewed_games()

#game_review = GameReview()
#game_review.write_review(1000, "false", "Recommended", "Dead by Daylight", "kkkkkkkkk kkk kkkkk")
#print(game_review.review_id)
#game_review.publish_review()
#show_latest_reviews("Dead by Daylight")


#show_latest_reviews("Dead by Daylight")
#search_review = GameReview()
#search_review.find_review_by_id(game_review.review_id)
#search_review.delete_review()
#show_latest_reviews("Dead by Daylight")

