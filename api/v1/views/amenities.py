#!/usr/bin/python3
"""
View for the amenities RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """ This function retrieves all amenities. Has no parameters. """
    amenity = []
    amenities = storage.all(Amenity).values()
    for value in amenities:
        amenity.append(value.to_dict())
    return jsonify(amenity)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_id_amenity(amenity_id):
    """ This function retrieves one amenity given an id. """
    obj = storage.get("Amenity", amenity_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_an_amenity(amenity_id):
    """ This function retrieves one amenity given an id and
        deletes it.
    """
    obj = storage.get("Amenity", amenity_id)
    if obj:
        obj.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/amenities/", methods=['POST'], strict_slashes=False)
def create_amenities():
    """ This function creates a new amenity. """
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")

    if new_amenity:
        if "name" not in new_amenity:
            abort(400, "Missing name")
        amenity = Amenity(**new_amenity)
        storage.new(ameninity)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenities_id>", methods=['PUT'],
                 strict_slashes=False)
def up_amenity(amenities_id):
    """ This function updates a amenity. """
    amenity = request.get_json()
    if not amenity:
        abort(400, "Not a JSON")

    obj = storage.get("Amenity", amenities_id)
    if obj:
        ignored_attr = ["id", "created_at", "updated_at"]
        for key, value in amenity_update.items():
            if key not in ignored_attr:
                setattr(obj, key, value)

            object_.save()
            storage.save()
        return make_response(jsonify(obj.to_dict()), 200)
    abort(404)
