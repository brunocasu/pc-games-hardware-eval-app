from component import create_cpu_component, create_gpu_component, update_component, delete_component, \
    get_gpu_stats_category, get_cpu_stats_category
from game_review import GameReview

# PC Components (Evaluation Functions)
# Managers: 2.	Create/update/delete a component information.
#cpu_id = create_cpu_component("AMD Ryzen Threadripper 5995WX", 100000, 3330, 9999.99, 64, 2023, "sWRX8", "Desktop")
#gpu_id = create_gpu_component("GeForce RTX 4090 Ti", 29000, 1117, 2099.99, 2023, "Desktop")
#update_component(gpu_id, {"category": "Server"})
#delete_component(cpu_id)
#delete_component(gpu_id)

# Managers: 1.	Create/update/delete a PC game information. TODO

# Managers: 3.	Delete a PC game review.
# search_review = GameReview()
# search_review.find_review_by_id("_id")
# search_review.delete_review()

# Statistics (Additional Functions)
# Managers: 4.	View statistics for Components, based on the categories.
# get_cpu_stats_category(2020)
# get_gpu_stats_category(2015)