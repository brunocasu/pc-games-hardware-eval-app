from component import create_cpu_component, create_gpu_component, update_component, \
    get_gpu_stats_category, get_cpu_stats_category
from system_requirements import create_system_requirement, update_system_requirement

# Management Demo 1 shows the use of the functions for additional statics on components and CRUD operations
# Statistics (Additional Functions)

# Managers: 4.	View statistics for Components, based on the categories.
get_cpu_stats_category(2020)
get_gpu_stats_category(2015)

# PC Components (Evaluation Functions)

# Managers: 2.	Create/update/delete a component information.
cpu_id = create_cpu_component("AMD Ryzen Threadripper 5995WX", 100000, 3330, 9999.99, 64, 2023, "sWRX8", "Desktop")
gpu_id = create_gpu_component("GeForce RTX 4090 Ti", 29000, 1117, 2099.99, 2023, "Desktop")
update_component(gpu_id, {"category": "Server"})

# Reviews and PC games requirements (Browsing Functions)

# Managers: 1.	Create/update/delete a PC game information.
create_system_requirement("Honkai: Star Rail", "8 GB", "Core i7-8700K", "GeForce GTX 1060", "Windows 10", "20 GB")
update_system_requirement("Honkai: Star Rail", {"File Size": "40 GB"})
