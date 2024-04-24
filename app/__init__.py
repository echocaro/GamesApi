from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from .routes.games_routes import games_routes

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

db = SQLAlchemy(app)

app.register_blueprint(games_routes, url_prefix="/game")
