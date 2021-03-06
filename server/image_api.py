from flask import Blueprint

image_api_blueprint = Blueprint('image_api', __name__)


@image_api_blueprint.route('/api/get_images')
def get_images():
    return "Hello"


@image_api_blueprint.route('/api/send_image')
def send_image():
    return "Hello"
