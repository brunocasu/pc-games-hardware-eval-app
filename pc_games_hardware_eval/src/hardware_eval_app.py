from component import Component
import uuid
from bson import Binary, UuidRepresentation

user_cpu = Component("cpu")
user_gpu = Component("gpu")

game_cpu = Component("cpu")
#game_gpu = Component("gpu")

user_cpu.find_component_by_name("Ryzen 5 3500X")

game_cpu.find_component_by_name("Core i3-8300")

if game_cpu.cpu.cpu_mark > user_cpu.cpu.cpu_mark:
    print("->User CPU does NOT meet the Game Requirements!")
    #game_cpu.suggest_upgrade(user_cpu.cpu.cpu_mark, user_cpu.category, 500)
#user_gpu.find_component_by_name("")