import os

from dotenv import load_dotenv
from flask import Flask

from .routes import main

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ["SECRET_KEY"]
    app.register_blueprint(main)
    return app
