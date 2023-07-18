
## !! Need Redis
def connect_to_app():
    print("->CONNECT To application...")
    # generate session number
    # REDIS: write session/1111/created_at: {datetime}
    # REDIS: write session/1111/game_searches: int

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

## OK
def show_best_value_components(limit, category, min_benchmark=0):
    print("->SHOW Compo")

## Mongo Need Class !! Need Redis
def search_game(game_name):
    print("->SEARCH Game Found in database!")
    # REDIS: read session/1111/user/cpu:
    # REDIS: read session/1111/user/gpu:
    # REDIS: read session/1111/game_searches:
    # REDIS: write session/1111/game_searches: +1

    #if component_id:
    # REDIS: write session/1111/user/game_eval/1/title: string
    # REDIS: write session/1111/user/game_eval/1/cpu: bool
    # REDIS: write session/1111/user/game_eval/1/gpu: bool

## OK
def search_component(game_name):
    print("->SEARCH Component Found in database!")

## OK
def post_review(hour_played, recommendation, title, new_review):
    print("->SEARCH Component Found in database!")
