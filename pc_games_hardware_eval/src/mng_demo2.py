from component import delete_component
from game_review import GameReview
from system_requirements import delete_system_requirement

# Management Demo 2 shows the use of the functions for removing documents from the DB

# Managers: 2.	Create/update/delete a component information.
delete_component("add_component_id")
delete_component("add_component_id")

# Managers: 3.	Delete a PC game review.
search_review = GameReview()
search_review.find_review_by_id("add_mongo_id")
search_review.delete_review()

# Managers: 1.	Create/update/delete a PC game information.
delete_system_requirement("Honkai: Star Rail")