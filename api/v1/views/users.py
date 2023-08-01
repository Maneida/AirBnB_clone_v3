#!/usr/bin/python3
"""RESTful API for the User class"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.user import User


@app_views('/api/v1/users',
           methods=['GET'], strict_slashes=False)
def get_user_list():
    """Retrieves list of all user objects"""
    user_list = [user.to_dict() for user in storage.all('User').values()]
    return jsonify(user_list)


@app_views('api/v1/users/<user_id>',
           methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a user object by user_id"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views('api/v1/users/<user_id>',
           methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object by user_id"""
    user = storage.get('User', user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views('api/v1/users',
           methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new User object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    elif "email" not in request.get_json():
        return jsonify({'error': 'Missing email'}), 400
    elif "password" not in request.get_json():
        return jsonify({'error': 'Missing password'}), 400
    else:
        obj_data = request.get_json()
        obj = User(**obj_data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views('api/v1/users/<user_id>',
           methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object by user_id"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 404

    obj = storage.get('User', user_id)
    if obj is None:
        return jsonify({'error': 'User not found'}), 404
    obj_data = request.get_json()
    ignore = ["id", "email", "created_at", "updated_at"]
    for key in obj_data.keys():
        if key in ignore:
            pass
        else:
            setattr(obj, key, obj_data[key])
    obj.save()
    return jsonify(obj.to_dict()), 200
