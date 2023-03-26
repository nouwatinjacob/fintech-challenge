from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
import sys
sys.path.append("..")
from config import Config
from flask_migrate import Migrate
from .utils.auth import auth_required

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db, command='migrate')

    from .api.users import UsersResource
    from .api.accounts import AccountResource
    api = Api(app)
    @app.get("/")
    @auth_required
    def home():
        return "WELCOME HERE!"
    api.add_resource(UsersResource, '/api/users', '/api/users/<int:user_id>')
    api.add_resource(AccountResource, '/api/accounts', '/api/accounts/<int:account_id>')

    SWAGGER_URL = '/api/docs'
    API_URL = '/api/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'My App'
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
