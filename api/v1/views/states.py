#!/usr/bin/python3
"""
View for the states RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    """ function that gets all the states """
    states = []
    all_ = storage.all(State).values()
    for value in all_:
        states.append(value.to_dict())
    return jsonify(states)

@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def state_by_id(state_id):
    """ function that get a state by his id """
    state = storage.get("State", state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)

@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """ function that deletes a state by his id """
    state = storage.get("State", state_id)
    if state:
        state.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)

@app_views.route("/states/", methods=['POST'], strict_slashes=False)
def create_state():
    """ function that create a new state """
    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")

    if new_state:
        if "name" not in new_state:
            abort(400, "Missing name")
        state = State(**new_state)
        storage.new(state)
        storage.save()
        return make_response(jsonify(state.to_dict()), 201)

@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def up_state(state_id):
    """ function that pudate a state by his id """
    state_up = request.get_json()
    if not state_up:
        abort(400, "Not a JSON")

    obj_ = storage.get(State, state_id)
    if obj_:
        ignored_attr = ["id", "created_at", "updated_at"]
        for key, value in state_up.items():
            if key not in ignored_attr:
                setattr(obj_, key, value)

            obj_.save()
        return make_response(jsonify(obj_.to_dict()), 200)

    abort(404)
    storage.save()
