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
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places), 200


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def place_by_id(place_id):
    """ function that gets a plece by the id """
    place = storage.get("Place", place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """ function that deletes a place"""
    place = storage.get("Place", place_id)
    if place:
        place.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ function that creates a new place. """
    new_place = request.get_json()
    if not new_place:
        abort(400, "Not a JSON")
    if not new_place.get("name"):
        abort(400, "Missing name")
    if not new_place.get("user_id"):
        abort(400, "Missing user_id")

    city = storage.get("City", city_id)
    if not storage.get("User", new_place.get("user_id")):
        abort(404)

    if not city:
        abort(404)

        place = Place(**new_place)
        setattr(place, "city_id", city_id)
        storage.new(place)
        storage.save()
        return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def up_places(place_id):
    """ function that updates a place. """
    place_up = request.get_json()
    if not place_up:
        abort(400, "Not a JSON")

    obj_ = storage.get(Place, place_id)
    if obj_:
        ignored_attr = ["id", "created_at", "updated_at"]
        for key, value in place_up.items():
            if key not in ignored_attr:
                setattr(obj_, key, value)

            obj_.save()
        return make_response(jsonify(obj_.to_dict()), 200)

    abort(404)
    storage.save()
