from flask import Flask


def init_blueprint(app):
    from app.entrypoints.flask_app.api import api

    app.register_blueprint(api, url_prefix="/api")


def create_app():
    app = Flask(__name__)
    init_blueprint(app)

    return app
