from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))


######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    """Return the health status of the service"""
    return jsonify(dict(status="OK")), 200


######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """Return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################


@app.route("/picture", methods=["GET"])
def get_pictures():
    """Retrieves all pictures from the database"""
    return jsonify(data)


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Retrieves a picture by it's picture ID"""
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture)
    return {"message":"Picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################


@app.route("/picture", methods=["POST"])
def create_picture():
    """Creates a new picture in the database"""
    new_picture = request.json
    if any(picture['id'] == new_picture['id'] for picture in data):
        return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302

    data.append(new_picture)
    return jsonify(new_picture), 201

        
######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Updates a picture in the database"""
    new_picture = request.json
    
    for picture in data:
        if picture['id'] == id:
            picture.update(new_picture)
            return jsonify(picture), 200
    return jsonify({'message': 'Picture not found'}), 404


######################################################################
# DELETE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Removes a picture from the database"""

    for i, picture in enumerate(data):
        if picture['id'] == id:
            del data[i]
            return jsonify({"message": "Picture deleted"}), 204
    return jsonify({"message": "Picture not found"}), 404
    