#!/usr/bin/python3
"""
RESTful API for the City class
"""
from api.v1.views import app_views
from flask import abort, Flask, jsonify, request, Blueprint
from models import storage
from models.city import City


@app_views.route('/api/v1/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_state_city_list(state_id):
    """GET city list by State given state_id"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities), 200


@app_views('/api/v1/cities/<city_id>',
           methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    """GET City object by city_id"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_dict()), 200


@app_views('api/v1/cities/<city_id>',
           methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """DELETE city obj by city_id

    Args:
        city_id (str): id of city object

    Returns:
        json: empty dict with status code 200 on success
        json: status code 404 if city_id is not linked to any City object
    """
    city = storage.get('City', city_id)
    if city is None:
        return jsonify({'error': 'City not found'}), 404
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views('api/v1/states/<state_id>/cities',
           methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a new city object for a specified State id"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    elif "name" not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    else:
        obj_data = request.get_json()
        state = storage.get('State', state_id)
        if state is None:
            return jsonify({'error': 'State not found'}), 404
        obj_data['state_id'] = state.id
        obj = City(**obj_data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views('api/v1/cities/<city_id>',
           methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object by city_id"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'})

    obj = storage.get('City', city_id)
    if obj is None:
        return jsonify({'error': 'City not found'}), 404

    obj_data = request.get_json()
    obj.name = obj_data['name']
    obj.save()
    return jsonify(obj.to_dict()), 200
