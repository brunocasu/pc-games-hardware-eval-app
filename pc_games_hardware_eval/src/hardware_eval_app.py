from component import Component
import uuid
from bson import Binary, UuidRepresentation

user_cpu = Component("cpu")
user_gpu = Component("gpu")

game_cpu = Component("cpu")
game_gpu = Component("gpu")

user_cpu.find_component_by_name("Core i5-9400F")
user_cpu.print_component_info()
game_cpu.find_component_by_name("Ryzen 5 3500")
game_cpu.print_component_info()

user_gpu.find_component_by_name("geforce gtx 950")
user_gpu.print_component_info()
game_gpu.find_component_by_name("Geforce gtx 1050 Ti")
game_gpu.print_component_info()

if game_cpu.cpu.cpu_mark > user_cpu.cpu.cpu_mark:
    print("->User CPU does NOT meet the Game Requirements!")
    #game_cpu.suggest_upgrade(user_cpu.cpu.cpu_mark, user_cpu.category, 500)

if game_gpu.gpu.g3d_mark > user_gpu.gpu.g3d_mark:
    print("->User GPU does NOT meet the Game Requirements!")
    game_gpu.suggest_upgrade(user_gpu.gpu.g3d_mark, user_gpu.category, 250)
#user_gpu.find_component_by_name("")