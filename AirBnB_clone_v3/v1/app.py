#!/usr/bin/python3
"""
Flask application module
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
    app.register_blueprint(app_views)

    @app.errorhandler(404)
    def page_not_found(e):
        """Handle 404 errors"""
        return jsonify(error="Not found"), 404

    @app.teardown_appcontext
    def teardown_db(exception):
        """Close the database connection"""
        storage.close()

    return app


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app = create_app()
    app.run(host=host, port=port, threaded=True)
