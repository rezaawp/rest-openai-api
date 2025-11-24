from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config.config import Config
import os
from controllers.upload_controller import upload_bp
from controllers.invoice_controller import invoice_handler
from extensions import db
from flask_restx import Api
from controllers.ai_video_controller import ai_video_ns, ai_video_callback_ns

migrate = Migrate()

def is_local_request():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    # API access only from LAN IP ranges
    allowed_prefix = (
        "127.",
        "192.168.",
        "10.",
        "172.16.", "172.17.", "172.18.", "172.19.",
        "172.20.", "172.21.", "172.22.", "172.23.",
        "172.24.", "172.25.", "172.26.", "172.27.",
        "172.28.", "172.29.", "172.30.", "172.31.",
    )

    return ip.startswith(allowed_prefix)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Restrict API access to LAN only
    @app.before_request
    def restrict_api():
        # allow static content for public
        if request.path.startswith("/static"):
            return

        # restrict only API routes
        if request.path.startswith("/api"):
            if not is_local_request():
                abort(403, description="API only accessible from local network.")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register RESTX API
    api = Api(
        app,
        version="1.0",
        title="Server API Documentation",
        description="Swagger UI for your Flask API",
        doc="/api/docs"  # Swagger UI endpoint
    )

    api.add_namespace(ai_video_ns, path="/api/ai")
    api.add_namespace(ai_video_callback_ns, path="/callback/ai")

    # Register blueprints
    app.register_blueprint(upload_bp, url_prefix="/api")
    app.register_blueprint(invoice_handler, url_prefix="/api")

    @app.route('/')
    def home():
        return "OpenAI API is running"

    return app


app = create_app()

port = int(os.getenv("PORT", 5000))
debug = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
if __name__ == '__main__':
    if (os.getenv("ENVIRONMENT") == "development"):
        print("Creating database tables...")
        with app.app_context():
            db.create_all()
    app.run(debug=debug, port=port)
