from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from .routes.games_routes import games_routes
from .models.db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

db.init_app(app)
Migrate(app, db)

app.register_blueprint(games_routes, url_prefix="/game")
