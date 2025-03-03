#!/usr/bin/python3
"""endpoint of state"""
from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=["GET", "POST"])
def get_states():
    """Retrieves the list of all State objects"""
    if request.method == 'GET':
        all_states = []

        for obj in storage.all("State").values():
            all_states.append(obj.to_dict())

        return jsonify(all_states)

    elif request.method == 'POST':
        http_data = request.get_json()
        if not http_data:
            return jsonify({"error": "Not a JSON"}), 400
        if "name" not in http_data:
            return jsonify({"error": "Missing name"}), 400

        new_state = State(**http_data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<string:state_id>', methods=["GET", "DELETE", "PUT"])
def stateid(state_id):
    """Retrieves, deletes or updates a State object by state_id"""
    if request.method == 'GET':
        for obj in storage.all("State").values():
            if obj.id == state_id:
                return jsonify(obj.to_dict())

    elif request.method == 'DELETE':
        for obj in storage.all("State").values():
            if obj.id == state_id:
                storage.delete(obj)
                storage.save()
                return jsonify({}), 200

    elif request.method == 'PUT':
        for obj in storage.all("State").values():
            if obj.id == state_id:
                http_data = request.get_json()
                if not http_data:
                    abort(400, 'Not a JSON')

                statics_attrs = ["id", "created_at", "updated_at"]
                for key, value in http_data.items():
                    if key not in statics_attrs:
                        setattr(obj, key, value)
                storage.save()
                return jsonify(obj.to_dict()), 200

    abort(404)
