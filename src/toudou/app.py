from flask import Flask
from toudou.api_view import api
from toudou.ihm_view import ihm
import toudou.models as models
from toudou.authy import auth
def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env(prefix='TOUDOU_FLASK')
    app.register_blueprint(ihm)
    app.register_blueprint(api)

    models.init_db()

    return app