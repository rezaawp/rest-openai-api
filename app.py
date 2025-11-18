from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config.config import Config
import os
from controllers.upload_controller import upload_bp
from extensions import db

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(upload_bp, url_prefix="/api")

    @app.route('/')
    def home():
        return "Invoice Management API running"

    return app


app = create_app()

port = int(os.getenv("PORT", 5000))
debug = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
if __name__ == '__main__':
    if (os.getenv("ENVIRONMENT") == "development"):
        print("Creating database tables...")
        with app.app_context():
            db.create_all()  # buat tabel langsung
    app.run(debug=debug, port=port)
