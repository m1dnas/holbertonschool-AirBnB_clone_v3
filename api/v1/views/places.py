#!/usr/bin/python3
''' Index python file '''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=["GET", "POST"])
def places_from_city(city_id):
    ''' Retrieves all cities from a state '''
    cities_list = [obj.to_dict() for obj in storage.all("City").values()]
    ids = [obj['id'] for obj in cities_list]
    if city_id in ids:
        if request.method == "GET":
            cities = storage.all("Place")
            city_places = [obj.to_dict() for obj in cities.values()
                           if obj.city_id == city_id]
            return jsonify(city_places)
        elif request.method == "POST":
            req_json = request.get_json()
            if not req_json:
                abort(400, 'Not a JSON')
            if not req_json.get("user_id"):
                abort(400, "Missing user_id")
            user = storage.get(User, req_json.get("user_id"))
            if not user:
                abort(404, "Not found")
            if 'name' not in req_json:
                abort(400, 'Missing name')
            req_json["city_id"] = city_id
            new_place = Place(**req_json)
            new_place.save()
            return jsonify(new_place.to_dict()), 201
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=["GET", "DELETE", "PUT"])
def place(place_id):
    ''' Retrieves, modifies, or deletes a particular place '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        if request.method == "GET":
            return jsonify(place.to_dict())
        if request.method == "DELETE":
            storage.delete(place)
            storage.save()
            return {}, 200
        elif request.method == "PUT":
            if not request.get_json():
                abort(400, 'Not a JSON')
            else:
                place = storage.get(Place, place_id)
                for key, value in request.get_json().items():
                    if key not in ['id', 'created_at',
                                   'updated_at', 'city_id', 'user_id']:
                        setattr(place, key, value)
                storage.save()
                return jsonify(place.to_dict()), 200