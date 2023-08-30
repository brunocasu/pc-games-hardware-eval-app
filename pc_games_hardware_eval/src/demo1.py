from hardware_eval_app import search_component, show_best_value_components, submit_my_system, evaluate_my_system

# PC Components (Evaluation Functions)

# Users: 5.	View a selected Component benchmarks and price.
search_component("cpu", "Ryzen 9 5950X")
search_component("gpu", "GeForce RTX 2080 Ti")
# Users: 6.	View the Components with the highest value metric.
show_best_value_components("cpu", "Laptop", min_benchmark=5000)
show_best_value_components("gpu", "Desktop", 3, 7000)
# Users: 7.	Submit its own System Configuration.
usr1 = submit_my_system("Core i5-9400F", "Geforce gtx 1050 Ti", 400)
usr2 = submit_my_system("Core i3-3225", "GeForce GTX 460", 250)
# Users: 9.	Obtain a System Evaluation
# Users: 10. Obtain a suggestion for a System Upgrade, based on a selected PC game.
evaluate_my_system(usr1, "Cyberpunk 2077")
evaluate_my_system(usr2, "Cyberpunk 2077")