from flask import Flask
from routes.route_medico import medico_bp
def create_app():
    app = Flask(__name__)

    app.register_blueprint(medico_bp)

    return app