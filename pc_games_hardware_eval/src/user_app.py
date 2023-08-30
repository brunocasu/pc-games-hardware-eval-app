from hardware_eval_app import search_component, show_best_value_components

# PC Components (Evaluation Functions)
# Users: 5.	View a selected Component benchmarks and price.
search_component("cpu", "Ryzen 9 5950X")
search_component("gpu", "GeForce RTX 2080 Ti")

# Users: 6.	View the Components with the highest value metric.
show_best_value_components("cpu", "Laptop", min_benchmark=5000)
show_best_value_components("gpu", "Desktop", 3, 7000)
