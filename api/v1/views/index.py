#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonifyi
from models import storage

@app_views.route('/', defaults={'page': 'index'})
@app_views.route('/<page>')
def api_status(page):
    """Get the status of the API.

    Returns:
        JSON object: {"status": "OK"}
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def api_stats():
    """Gets stat of all class data"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    all_cls = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]
    stats_dict = {}

    for i in range(len(all_cls)):
        stats_dict[names[i]] = storage.count(all_cls[i])
    return jsonify(stats_dict)
