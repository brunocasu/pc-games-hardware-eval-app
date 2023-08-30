from component import Component
from session import UserSession, Evaluation
from component import get_gpu_stats_category, \
    get_cpu_stats_category, show_best_cpu_value, show_best_gpu_value
from game_review import GameReview
from game_review import show_most_reviewed_games, show_best_reviewed_games, show_latest_reviews
import uuid
from bson import Binary, UuidRepresentation
from system_requirements import GameRequirements


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


# Users: 7.	Submit its own System Configuration.
def submit_my_system(cpu_name, gpu_name, budget):
    usr = UserSession()
    usr.create_session_kv()
    usr.submit_system_kv(cpu_name, gpu_name, budget)
    return usr


# Users: 9.	Obtain a System Evaluation
# Users: 10. Obtain a suggestion for a System Upgrade, based on a selected PC game.
def evaluate_my_system(usr_obj, game_title):
    usr_obj.n_searches = usr_obj.n_searches + 1
    eval = Evaluation(usr_obj.session_id, usr_obj.n_searches, game_title)
    eval.get_system_evaluation()


# Users: 4.	View the System Requirements for a selected PC game.
def search_game_requirements(title):
    gg = GameRequirements(title)
    gg.find_game_requirements()


# Users: 8.	Submit a simple review of a PC game.
def write_my_review(hours_played, is_early_access, recommend, game_title, review_text):
    review_obj = GameReview()
    review_obj.write_review(hours_played, is_early_access, recommend, game_title, review_text)
    return review_obj


def submit_my_review(review_obj):
    review_obj.publish_review()

# Managers: 1.	Create/update/delete a PC game information. TODO


