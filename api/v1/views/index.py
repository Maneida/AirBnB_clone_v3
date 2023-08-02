#!/usr/bin/python3
""" Index api methods
    Contains:
        api_status: for checking status of API
        api_stats: for getting stats of each Class
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/', defaults={'page': 'index'})
@app_views.route('/status',
                 methods=['GET'], strict_slashes=False)
def api_status():
    """Get the status of the API.

    Returns:
        JSON object: {"status": "OK"}
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def api_stats():
    """Gets stat of all class data
       Returns:
            JSON object: { "Class": count }
    """

    all_cls = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]
    stats_dict = {}

    for i in range(len(all_cls)):
        stats_dict[names[i]] = storage.count(all_cls[i])
    return jsonify(stats_dict)
