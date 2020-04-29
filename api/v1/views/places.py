#!/usr/bin/python3
"""Place page for flask that displays class places."""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """ function that get all places in cities. """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places_list = [p.to_dict() for p in city.places]
    return jsonify(places_list), 200


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def place_by_id(place_id):
    """ function that gets a plece by the id """
    obj = storage.get("Place", place_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """ function that deletes a place"""
    obj = storage.get("Place", place_id)
    if obj:
        obj.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def new_place(city_id):
    """ function that creates a new place. """
    n_place = request.get_json()
    if not n_place:
        abort(400, "Not a JSON")
    if not n_place.get("name"):
        abort(400, "Missing name")
    if not n_place.get("user_id"):
        abort(400, "Missing user_id")

    city = storage.get("City", city_id)
    if not storage.get("User", new_place.get("user_id")):
        abort(404)

    if not city:
        abort(404)

    p = Place(**new_place)
    setattr(p, "city_id", city_id)
    storage.new(p)
    storage.save()
    return make_response(jsonify(p.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def up_places(place_id):
    """ function that updates a place. """
    place_up = request.get_json()
    if not place_up:
        abort(400, "Not a JSON")

    obj = storage.get("Place", place_id)
    if obj:
        no_mod = ["id", "created_at", "updated_at"]
        for key, value in place_up.items():
            if key not in no_mod:
                setattr(obj, key, value)

            obj.save()
            storage.save()
        return make_response(jsonify(obj.to_dict()), 200)
    abort(404)
