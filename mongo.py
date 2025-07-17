# mongo.py
from datetime import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["steam_games_db"]
collection = db["games"]

def insert_game(email: str, game_data: dict):
    game_data["name"] = game_data["name"].lower()
    game_data["last_updated"] = datetime.utcnow()

    # Check if game already exists with this user
    existing = collection.find_one({
        "email": email,
        "game.name": game_data["name"]
    })

    if existing:
        old_price = existing["game"]["price"]
        if old_price != game_data["price"]:
            # Price changed — update price and push to history
            collection.update_one(
                {"email": email, "game.name": game_data["name"]},
                {
                    "$set": {
                        "game.price": game_data["price"],
                        "game.last_updated": game_data["last_updated"]
                    },
                    "$push": {
                        "game.price_history": {
                            "price": game_data["price"],
                            "date": game_data["last_updated"]
                        }
                    }
                }
            )
            return "Price updated"
        else:
            # No price change — just update timestamp
            collection.update_one(
                {"email": email, "game.name": game_data["name"]},
                {
                    "$set": {
                        "game.last_updated": game_data["last_updated"]
                    }
                }
            )
            return "No change"
    
    # If not exists — create new with initial price history
    game_data["price_history"] = [{
        "price": game_data["price"],
        "date": game_data["last_updated"]
    }]
    collection.insert_one({
        "email": email,
        "game": game_data
    })
    return "Game added"


def get_all_games():
    return list(collection.find({}, {"_id": 0}))

# def get_game_by_email_and_name(email: str, name: str):
#     name = name.lower()

#     doc = collection.find_one(
#         {"email": email, "game.name": name},
#         {"_id": 0, "game": 1}
#     )
#     print(doc)
#     return doc["game"] if doc else None

def get_game_by_email_and_name(email: str, name: str):
    name = name.lower()
    
    print(f" Searching for game '{name}' for user '{email}'")

    doc = collection.find_one(
        {"email": email, "game.name": name},
        {"_id": 0, "game": 1}
    )
    
    print("📄 Result found:", doc)
    return doc["game"] if doc else None
