from component import Component
from component import get_gpu_stats_category, \
    get_cpu_stats_category, show_best_cpu_value, show_best_gpu_value,\
    create_cpu_component, update_component, delete_component
import uuid
from bson import Binary, UuidRepresentation

user_cpu = Component("cpu")
user_gpu = Component("gpu")

game_cpu = Component("cpu")
game_gpu = Component("gpu")

user_cpu.find_component_by_name("Core i5-9400F")
user_cpu.print_component_info()
game_cpu.find_component_by_name("Ryzen 7 5700U")
game_cpu.print_component_info()

user_gpu.find_component_by_name("geforce gtx 950")
user_gpu.print_component_info()
game_gpu.find_component_by_name("Geforce gtx 1050 Ti")
game_gpu.print_component_info()

if game_cpu.cpu.cpu_mark > user_cpu.cpu.cpu_mark:
    print("->User CPU does NOT meet the Game Requirements!")
    game_cpu.suggest_upgrade(user_cpu.cpu.cpu_mark, user_cpu.category, 500)

if game_gpu.gpu.g3d_mark > user_gpu.gpu.g3d_mark:
    print("->User GPU does NOT meet the Game Requirements!")
    game_gpu.suggest_upgrade(user_gpu.gpu.g3d_mark, user_gpu.category, 230)

get_cpu_stats_category(2020)
get_gpu_stats_category(2015)
show_best_cpu_value(5, "Desktop, Laptop", 8000)
show_best_gpu_value(5, "Desktop")

#component_uuid = create_cpu_component("AMD Ryzen Threadripper 5995WX", 100000, 3330, 64, 2023, "sWRX8", "Desktop")
#update_component(component_uuid, {"category": "Server"})
#update_component("758847ba-b1d2-46df-bc32-1147338c35dc", {"testing": "test"})
#delete_component("758847ba-b1d2-46df-bc32-1147338c35dc")