from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes import auth_routes

    app.register_blueprint(auth_routes.bp)

    return app