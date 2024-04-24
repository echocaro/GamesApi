from flask import Blueprint, jsonify, request
import json
from app.models.db import db
from app.models.games import Game
import os
import requests

API_KEY = os.environ.get('API_KEY')
RAWG_API_URL = 'https://api.rawg.io/api/games'
games_routes = Blueprint("games_routes", __name__)


@games_routes.route('/<string:name>', methods=["GET"])
def get_game_by_name(name):
    if not name:
        return jsonify({"error": "No game name was provided"}), 400

    params = {
        'key': API_KEY,
        'search': name
    }
    response = requests.get(RAWG_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return jsonify(extract_game_details(data)), 200
    else:
        return jsonify(response.json()), response.status_code


# gets all games
@games_routes.route("/", methods=["GET"])
def get_all_games():
    page = request.args.get('page', 1)
    page_size = request.args.get('page_size', 20)

    params = {
        'key': API_KEY,
        'page': page,
        'page_size': page_size
    }

    response = requests.get(RAWG_API_URL, params=params)

    if response.status_code == 200:
        # need to get just the necessary details
        data = response.json()
        return jsonify(data)
    else:
        return jsonify(response.json()), response.status_code


def extract_game_details(data):
    results = data.get('results')

    if results and len(results) > 0:
        first_result = results[0]

        game_details = {
            "name": first_result.get("name"),
            "release_date": first_result.get("released"),
            "first_genre": first_result['genres'][0]['name'] if first_result.get('genres') else "",
            "stores": [store['store']['name'] for store in first_result.get('stores', [])]
        }

        return game_details

    return {'error': 'No games found'}
