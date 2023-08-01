#!/usr/bin/python3
"""
    App for registering blueprint and starting flask
"""
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from flask import jsonify
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception=None):
    """Close the database storage connection after each request.

    Args:
        exception (Exception): The exception that occurred, if any.
    """
    storage.close


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
