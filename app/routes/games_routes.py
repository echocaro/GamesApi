from flask import Blueprint, jsonify, request
import json
from app.models.db import db
from app.models.games import Game
import os
import requests

API_KEY = os.environ.get('API_KEY')
RAWG_API_URL = 'https://api.rawg.io/api/games'
games_routes = Blueprint("games_routes", __name__)


# get first game on the list
@games_routes.route('/<string:name>', methods=["GET"])
def get_game_by_name(name):
    if not name:
        return jsonify({"error": "No game name was provided"}), 400

    params = {
        'key': API_KEY,
        # 'search': name
    }
    response = requests.get(RAWG_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return jsonify(extract_game_details(data, False)), 200
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
        data = response.json()
        return jsonify(extract_game_details(data))
    else:
        return jsonify(response.json()), response.status_code


@games_routes.route('/<int:id>', methods=["POST"])
def create_game(id):
    params = {
        'key': API_KEY,
    }

    response = requests.get(f'{RAWG_API_URL}/{id}', params=params)

    if response.status_code == 200:
        data = response.json()

        extracted_details = {
            "name": data.get("name"),
            "release_date": data.get("released"),
            "first_genre": data['genres'][0]['name'] if data.get('genres') else "",
            "stores": [store['store']['name'] for store in data.get('stores', [])]
        }

        new_game = Game(name=extracted_details['name'],
                        genre=extracted_details['first_genre'], release_date=extracted_details['release_date'], stores=extracted_details['stores'])

        db.session.add(new_game)
        db.session.commit()
        return jsonify({'message': 'Game created successfully'}), 201
    else:
        return jsonify(response.json()), response.status_code


def extract_game_details(data, all_games=True):
    results = data.get('results')

    if all_games == True:

        if results and len(results) > 0:
            games = []

            for result in results:
                game_detail = {
                    "id": result.get("id"),
                    "name": result.get("name"),
                    "release_date": result.get("released"),
                    "first_genre": result["genres"][0]['name'] if result.get("generes") else "",
                    "stores": [store['store']['name'] for store in result.get('stores', [])]
                }
                games.append(game_detail)

            return games

    else:
        if results and len(results) > 0:
            first_result = results[0]

            game_details = {
                "id": first_result.get("id"),
                "name": first_result.get("name"),
                "release_date": first_result.get("released"),
                "first_genre": first_result['genres'][0]['name'] if first_result.get('genres') else "",
                "stores": [store['store']['name'] for store in first_result.get('stores', [])]
            }

            return game_details

    return {'error': 'No games found'}
