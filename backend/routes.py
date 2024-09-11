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
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for picture in data:
            if picture['id'] == id:
                return jsonify(picture), 200
        return {"message": "No matching picture id was found"}, 404

    return {"message": "Internal server error"}, 500


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    if data:
        picture_json = request.json
        new_id = picture_json['id']
        for picture in data:
            if new_id == picture['id']:
                message_payload = "picture with id " + str(picture['id']) + " already present"
                return {"Message": message_payload }, 302 
        data.append(picture_json)
        return {"Message": "picture added successfully!", "id": new_id}, 201
    return {"message": "Internal server error"}, 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    if data:
        picture_json = request.json
        for picture in data:
            if id == picture['id']:
                oldIndex = data.index(picture)
                data[oldIndex] = picture_json
                message_payload = "picture with id " + str(picture['id']) + " successfully updated"
                return {"Message": message_payload }, 200 

        return {"Message": "picture not found"}, 404
    return {"message": "Internal server error"}, 500

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if data:
        for picture in data:
            if id == picture['id']:
                index = data.index(picture)
                del data[index]
                return {}, 204

        return {"message": "picture not found"}, 404
    return {"message": "Internal server error"}, 500
