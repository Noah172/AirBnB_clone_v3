#!/usr/bin/python3
"""
View for the amenities RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenities():
    """ function that gets all the states """
    amenities = []
    all_ = storage.all(Amenity).values()
    for amenity in all_:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """ function thar get amenity by id. """
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """ function that delete an amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/amenities/", methods=['POST'], strict_slashes=False)
def create_amenity():
    """ function that creates a new amenity. """
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")

    if new_amenity:
        if "name" not in new_amenity:
            abort(400, "Missing name")
        amenity = Amenity(**new_amenity)
        storage.new(amenity)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenities_id>", methods=['PUT'],
                 strict_slashes=False)
def up_amenity(amenities_id):
    """ function that updates a amenity. """
    amenity_up = request.get_json()
    if not amenity_up:
        abort(400, "Not a JSON")

    obj_ = storage.get(Amenity, amenities_id)
    if obj_:
        ignored_attr = ["id", "created_at", "updated_at"]
        for key, value in amenity_up.items():
            if key not in ignored_attr:
                setattr(obj_, key, value)

            obj_.save()
        return make_response(jsonify(obj_.to_dict()), 200)

    abort(404)
    storage.save()
