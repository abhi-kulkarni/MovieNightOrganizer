from flask import Flask
import flask
import os
import json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

env = os.environ.get

class Config:
    LOCALE = env("MOVIE_NIGHT_ORGANIZER_LOCALE", 'en_US.utf8')
    SECRET_KEY = env("MOVIE_NIGHT_ORGANIZER_SECRET_KEY",
                     "\xbe\x07Sw,h.\x81\xdb\x7f\x18\xb0j\xf1\xfd=`_\xb5\xb3\xb3\x15\xefNks\x991}\x12m\xc8")
    SQLALCHEMY_DATABASE_URI = env(
        "MOVIE_NIGHT_ORGANIZER_SQL_ALCHEMY_DATABASE_URI", "mysql://root:Windows18!@localhost/movie_night_organizer")

app = Flask(__name__)

app.config.from_object(Config())

db = SQLAlchemy(app)

db.init_app(app)

cors = CORS(app, allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials", "withCredentials"],
            supports_credentials=True, resources={r"/*": {"origins": "*"}})

from views import friend_views, movie_list_views

if __name__ == '__main__':
    app.run()
