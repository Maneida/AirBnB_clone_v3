#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/', defaults={'page': 'index'})
@app_views.route('/<page>')
def api_status(page):
    """Get the status of the API.

    Returns:
        JSON object: {"status": "OK"}
    """
    return jsonify({"status": "OK"})
