import os
from flask import Blueprint, request, Response
import csv
from datetime import datetime

image_api_blueprint = Blueprint("image_api", __name__)


# In the query ? there should be sa sorting section
# We can cache the sorted results and only sort when new pics are added
# The URLs can be stored in a CSV file
@image_api_blueprint.route("/api/get_images")
def get_images():
    sorting_mode = request.args.get("sortby")

    if sorting_mode == None:
        sorting_mode = "date"
    elif sorting_mode not in ["date", "votes"]:
        return Response(status=400)

    return "Hello"


@image_api_blueprint.route("/api/send_image", methods=["POST"])
def send_image():
    # TODO: Verify with Recaptcha
    if not request.is_json:
        return Response(status=400)

    try:
        image_url = request.get_json()["image_url"]
    except KeyError:
        return Response(status=400)

    if not os.path.exists("./data/stored_images.csv"):
        f = open("./data/stored_images.csv", "w")
        f.close()

    with open("data/stored_images.csv", "w") as f:
        csv_writer = csv.writer(
            f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([image_url, datetime.now()])

    return Response(status=201)
