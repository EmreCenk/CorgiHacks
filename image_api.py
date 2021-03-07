import os
from flask import Blueprint, request, Response
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import func, desc
from datetime import datetime
import pymongo

image_api_blueprint = Blueprint("image_api", __name__)

# Config database
mongodb_uri = "mongodb+srv://Callum:Clammy753@corgihacks.z3vll.mongodb.net/Images?retryWrites=true&w=majority"
mongo_client = pymongo.MongoClient(mongodb_uri)
db = mongo_client.test
image_db = db.Images


def create_database_entry(submitter_name, dog_name, image_url):
    # print(image_db.find().sort("submission_id",
    #                            pymongo.DESCENDING).limit(1)[0])
    submission_id = image_db.find().sort(
        "submission_id", pymongo.DESCENDING).limit(1)
    if submission_id.count() == 0:
        submission_id = 0
    else:
        submission_id = submission_id[0]["submission_id"] + 1

    submission = {"submission_id": submission_id, "submitter_name":  submitter_name,
                  "dog_name": dog_name, "image_url": image_url, "number_of_votes": 0}
    return submission


@ image_api_blueprint.route("/api/vote_image", methods=["POST"])
def vote_image():
    if not request.is_json:
        return Response(status=400)

    try:
        request_content = request.get_json()
        submission_id = request_content["submission_id"]
    except KeyError:
        return Response(status=400)

    image_db.update_one({"submission_id": submission_id},
                        {"$inc": {"number_of_votes": 1}})
    return Response(status=200)


@ image_api_blueprint.route("/api/send_image", methods=["POST"])
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

    submission = create_database_entry(submitter_name, dog_name, image_url)
    image_db.insert_one(submission)

    return Response(status=200)


# In the query ? there should be a sorting section
@ image_api_blueprint.route("/api/get_images", methods=["GET"])
def get_images():
    sorting_mode = request.args.get("sortby")

    if sorting_mode == None:
        sorting_mode = "date"
    elif sorting_mode not in ["date", "votes"]:
        return Response(status=400)

    if sorting_mode == "votes":
        # If sorting mode is votes, give them the top 50
        query_content = image_db.find().sort(
            "number_of_votes", pymongo.DESCENDING).limit(50)[0:50]
        # Make query_content JSON serializable with list comprehension
        query_content = [{"submission_id": x["submission_id"],
                          "dog_name": x["dog_name"],
                          "submitter_name": x["submitter_name"],
                          "image_url": x["image_url"],
                          "number_of_votes": x["number_of_votes"]}
                         for x in query_content]
        list_response = {"content": query_content}
        return list_response
    else:
        # Get 25 images in order of submission_id descending based on starting ID
        start_point = int(request.args.get("start")) or 0
        submission_id = image_db.find().sort(
            "submission_id", pymongo.DESCENDING).limit(1)

        if submission_id.count() == 0:
            submission_id = 0
        else:
            submission_id = submission_id[0]["submission_id"] + 1

        query_content = image_db.find({"submission_id": {"$lt": submission_id - start_point}}).sort(
            "submission_id", pymongo.DESCENDING).limit(50)[0:50]

        query_content = [{"submission_id": x["submission_id"],
                          "dog_name": x["dog_name"],
                          "submitter_name": x["submitter_name"],
                          "image_url": x["image_url"],
                          "number_of_votes": x["number_of_votes"]}
                         for x in query_content]
        list_response = {"content": query_content}
        return list_response
