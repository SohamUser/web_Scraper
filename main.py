# main.py
from fastapi import FastAPI, Query
from sel import scrape_steam_game
from mongo import insert_game, get_all_games , get_game_by_email_and_name
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:3000",  
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         
    allow_credentials=True,
    allow_methods=["*"],          
    allow_headers=["*"],           
)
class ScrapeRequest(BaseModel):
    url: str
    email: str

@app.get("/")
def root():
    return {"message": "Steam Game Scraper API"}

@app.post("/scrape")
def scrape(request: ScrapeRequest):
    game_data = scrape_steam_game(request.url)
    result = insert_game(request.email, game_data)
    return {"status": result, "data": game_data}

@app.get("/games")
def get_games():
    return get_all_games()

@app.get("/track/price")
def get_tracked_price(email: str = Query(...), name: str = Query(...)):
    game = get_game_by_email_and_name(email, name)
    if not game:
        return {"error": "Game not found"}, 404

    return {
        "email": email,
        "game_name": game["name"],
        "platform": game["platform"],
        "price": game["price"],
        "image": game["image"],
        "url": game["url"],
        "description": game["description"],
        "release_date": game["release_date"],
        "last_updated": game["last_updated"],
        "price_history": game.get("price_history", [])
    }