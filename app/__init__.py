from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from app.config import Config
from app.extensions import db, migrate, login_manager, csrf


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Trust proxy headers (Cloudflare Tunnel / reverse proxy)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Flask-Session with SQLAlchemy backend
    app.config["SESSION_SQLALCHEMY"] = db

    # Register blueprints
    from app.blueprints.auth import bp as auth_bp
    from app.blueprints.habits import bp as habits_bp
    from app.blueprints.dashboard import bp as dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(habits_bp)
    app.register_blueprint(dashboard_bp)

    # User loader
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    return app
