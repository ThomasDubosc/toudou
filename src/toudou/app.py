import os

from flask import Flask

from toudou.api.api_view import api
from toudou.auth.auth_view import auth
from toudou.crud.crud_view import crud
import toudou.models as models

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env(prefix='TOUDOU_FLASK')
    app.register_blueprint(crud)
    app.register_blueprint(api)
    app.register_blueprint(auth)


    @app.before_first_request
    def init_db():
        models.init_db()

    return app

