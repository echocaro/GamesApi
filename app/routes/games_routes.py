from flask import Blueprint, jsonify
import json
from app.models.db import db
from app.models.games import Game
import os

API_KEY = os.environ.get('API_KEY')
RAWG_API_URL = 'https://api.rawg.io/api/games'
games_routes = Blueprint("games_routes", __name__)

@games_routes.route('/<string:name>', methods=["GET"])
def get_game_by_name(name):
  print("name")
  print(name)
  if not name:
    return jsonify({"error": "No game name was provided"}), 400

  response = requests.get(RAWG_API_URL, params={ 'key': RAWG_API_URL, 'search': name})

  print("response")
  print(response)
  data = response.json()
