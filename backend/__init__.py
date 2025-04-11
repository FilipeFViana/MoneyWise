import os
from flask import Flask
from backend.extensions import db, jwt
from dotenv import load_dotenv



def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    templates = os.path.join(base_dir, "..", "templates")
    static = os.path.join(base_dir, "..", "static")

    app = Flask(__name__, template_folder=templates, static_folder=static)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moneywise.db"
    app.config["JWT_SECRET_KEY"] = "supersecreto"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 1800

    db.init_app(app)
    jwt.init_app(app)

    from backend.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    with app.app_context():
        db.create_all()
        load_dotenv()
    return app
