import os
from flask import Blueprint, request, Response, current_app
from flask_sqlalchemy import SQLAlchemy
import csv
from datetime import datetime

image_api_blueprint = Blueprint("image_api", __name__)

db = SQLAlchemy()


class Image(db.Model):
    submission_id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(100))
    submitter_name = db.Column(db.String(100))
    dog_name = db.Column(db.String(100))
    date_submitted = db.Column(db.DateTime, default=datetime.now)
    number_of_votes = db.Column(db.Integer, default=0)


@image_api_blueprint.route("/api/send_image", methods=["POST"])
def send_image():
    # TODO: Verify with Recaptcha
    if not request.is_json:
        return Response(status=400)

    try:
        request_content = request.get_json()
        image_url = request_content["image_url"]
        submitter_name = request_content["submitter_name"]
        dog_name = request_content["dog_name"]
    except KeyError:
        return Response(status=400)

    # Set submission ID to max in db + 1
    image = Image(submission_id=0, image_url=image_url,
                  submitter_name=submitter_name, dog_name=dog_name)
    db.session.add(image)
    db.session.commit()

    return Response(status=200)


# In the query ? there should be a sorting section
@image_api_blueprint.route("/api/get_images", methods=["GET"])
def get_images():
    sorting_mode = request.args.get("sortby")

    if sorting_mode == None:
        sorting_mode = "date"
    elif sorting_mode not in ["date", "votes"]:
        return Response(status=400)

    return "Hello"
