from game_review import show_most_reviewed_games, show_best_reviewed_games, show_latest_reviews
from hardware_eval_app import search_game_requirements, write_my_review, submit_my_review
from system_requirements import show_embedded_reviews

# Demo 2 shows the use of the functions when a User wants to browse trending Games and check its requirements
# Also, the functions for seeing and posting reviews for the games
# Reviews and PC games requirements (Browsing Functions)

# Users: 4.	View the System Requirements for a selected PC game.
search_game_requirements("Dead by Daylight")
search_game_requirements("Valorant")
# Users: 1.	View most reviewed PC games.
show_most_reviewed_games(3)
# Users: 2.	View best reviewed PC games.
show_best_reviewed_games(3)
# Users: 3.	View the latest reviews of a selected PC game.
show_latest_reviews("Dead by Daylight", 3)
show_embedded_reviews("Dead by Daylight")
# Users: 8.	Submit a simple review of a PC game.
new_review = write_my_review(1000, "false", "Recommended", "Dead by Daylight", "good game!")
submit_my_review(new_review)
show_embedded_reviews("Dead by Daylight")