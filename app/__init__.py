from flask import Flask

from config import Config
from app.extensions import db, socketio, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    socketio.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints here
    from app.chat import bp as chat_bp
    from app.users import bp as user_bp
    app.register_blueprint(chat_bp)
    app.register_blueprint(user_bp)

    with app.app_context():
        from app.models import User, Room, Message, UsersRooms

    return app
