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
    """ function that get all the amenities"""
    amenities = []
    all_amenities = storage.all(Amenity).values()
    for amenity in all_amenities:
        amenities.append(amenity.to_dic())
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """ function that get an amenity by the id """
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    return (404)


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
def new_amenity():
    """ function that creates a new amenity """
    new = request.get_json()
    if not new:
        abort(400, "not a JSON")
    else:
        if "name" not in new:
            abort(400, "Missing name")
        amenity = Amenity(**new_amenity)
        storage.new(amenity)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenities_id>", methods=['PUT'],
                 strict_slashes=False)
def up_amenity(amenity_id):
    """ function that updates an amenity """
    amenity = request.get_json()
    if not amenity:
        abort(400, "Not a JSON")

    obj = storage.get("Amenity", amenity_id)
    if obj:
        no_mod = ["id", "created_at", "updated_at"]
        for key, value in amenity.items():
            if key not in no_mod:
                setattr(obj, key, value)
            obj.save()
            storage.save()
        return make_response(jsonify(obj.to_dict()), 200)
    abort(404)
