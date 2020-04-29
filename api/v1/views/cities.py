#!/usr/bin/python3
"""View for the city RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id=None):
    """
    Takes a state id and queries storare for cities that belong to that state

    Args:
        state_id: id of state to search cities

    Returns:
        list of cities by state in json format
    """
    state = storage.get(State, state_id)
    if state:
        cities = []
        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id=None):
    """
    Takes a string and queries storgae for a state with that id,
    if found creates a city with the info recieve in the body of the request

    Args:
        state_id: state that city is located in

    Returns:
        The data of the new city with status code 201
    """

    state = storage.get(State, state_id)
    if state:
        try:
            data = request.get_json()
        except:
            abort(400, 'Not a JSON')
        if 'name' in data.keys():
            data['state_id'] = state_id
            new_city = City(**data)
            storage.new(new_city)
            try:
                storage.save()
            except:
                abort(404)
            return jsonify(new_city.to_dict()), 201
        else:
            abort(400, 'Missing name')
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id=None):
    """
    Takes an id and queries storage for a city with that id

    Args:
        city_id: id of city to find

    Returns:
        City data in json format
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id=None):
    """
    Takes an id and if a city with that id is found deletes it

    Args:
        city_id: id of city to delete

    Returns:
        empty json with status code 200
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id=None):
    """
        Takes an id, queries the storage for a city with that id and if found,
        updates it with the info in the body

        Args:
            city_id: id of the city to update

        Returns:
            The data of the updated city with status code 200
    """

    city = storage.get(City, city_id)
    if city:
        try:
            req_body = request.get_json()
        except:
            abort(400, 'Not a JSON')
        keys_ignore = ['id', 'state_id', 'created_at', 'updated_at']
        for key in req_body.keys():
            if key not in keys_ignore:
                setattr(city, key, req_body[key])
        storage.save()
        return jsonify(city.to_dict())        
        return 'ok'
    else:
        abort(404)
