#!/usr/bin/python3
"""Api view to manage states requests"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def api_states_no_id():
    """Handles Get and Post api request on states"""

    states = storage.all(State)

    if request.method == 'GET':
        all_states = []
        for state in states.values():
            all_states.append(state.to_dict())
        return jsonify(all_states)

    elif request.method == 'POST':
        if not request.get_json():
            abort(400, description='Not a JSON')
        elif 'name' not in request.get_json():
            abort(400, description='Missing name')
        request_body = request.get_json()
        new = State(**request_body)
        storage.new(new)
        storage.save()
        return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def api_states(state_id):
    """Handles Get, Put, and Delete api request on states corresponding id"""

    states = storage.all(State)

    if request.method == 'GET':
        key = 'State' + '.' + state_id
        try:
            return jsonify(states[key].to_dict())
        except KeyError:
            abort(404)

    elif request.method == 'DELETE':
        state = storage.get(State, state_id)
        if state:
            storage.delete(state)
            storage.save()
            return make_response(jsonify({}), 200)
        else:
            abort(404)
    elif request.method = ['PUT']:
        key = 'State' + '.' + state_id

        try:
            state = states[key]

            if not request.get_json():
                abort(404, 'Not a JSON')
            else:
                data = request.get_json()
                no_put = ['id', 'updated_at', 'created_at']

                for key, value in data.items():
                    if key not in no_put:
                        setattr(state, key, value)
                storage.save()
                return make_response(jsonify(state.to_dict()), 200)
        except KeyError:
            abort(404)
    else:
        abort(501)
