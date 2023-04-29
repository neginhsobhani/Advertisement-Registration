# ّFirst API, Cloud Computing project
import json
import os
from flask import Flask, request, jsonify, abort
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
import pathlib
import s3module
import rabbitMQ_send
import mongodb_module

app = Flask(__name__)


def check_input(input_email, input_description, input_image):
    invalid_inputs = []
    if input_email == "" or not isinstance(input_email, str):
        invalid_inputs.append('Invalid email ')
    if input_description == "" or not isinstance(input_description, str):
        invalid_inputs.append('Invalid description ')
    if input_image.filename == '':
        invalid_inputs.append('No selected file ')

    if len(invalid_inputs) != 0:
        message = "".join(invalid_inputs)
        abort(404, description=message)
    else:
        return True


def save_image(image_file, image_id):
    file_extension = pathlib.Path(secure_filename(image_file.filename)).suffix
    new_file_name = str(image_id) + str(file_extension)
    image_file.save(secure_filename(new_file_name))
    return secure_filename(new_file_name)


@app.route("/getAd", methods=["GET"])
def get_advertisement():
    ad_id = int(request.args.get('id'))
    ad_doc = mongodb_module.get_ad_by_id(ad_id)
    if ad_doc is not None:
        ad_state = ad_doc['state']
        if ad_state == 'processing':
            return 'Your advertisement is still in processing queue'
        elif ad_state == 'rejected':
            return 'You advertisement was rejected'
        elif ad_state == 'approved':
            response = {
                "id": ad_doc['id'],
                "email": ad_doc['email'],
                "description": ad_doc['description'],
                "image_url": ad_doc['url'],
                "category": ad_doc['category'],
                "state": ad_doc['state']
            }
            return response
    else:
        return 'Advertisement with this id does not exist'


@app.route("/postAd", methods=["POST"])
def post_advertisement():
    if request.method == "POST":
        input_email = request.form["email"]
        input_image = request.files["file"]
        input_description = request.form["description"]

        # checking input
        input_is_valid = check_input(input_email, input_description, input_image)

        if input_is_valid:
            # calculate id of the new advertisement
            new_ad_id = mongodb_module.generate_new_id()

            # save the input image
            file_name = save_image(input_image, new_ad_id)

            # save image to s3
            absolute_file_path = str(pathlib.Path().absolute())
            new_ab = absolute_file_path.replace('\\', '/')
            file_path = new_ab + "/" + str(file_name)
            file_object = str(file_name)

            # upload the image to s3 and obtain image saved in s3
            url = s3module.upload_to_s3(file_path, file_object)
            os.remove(file_object)
            # write information in database
            mongodb_module.insert_new_ad(new_ad_id, input_email, input_description, url)

            # send advertisement id to rabbitMQ
            rabbitMQ_send.rabbitmq_send(str(new_ad_id))

            return 'your advertisement was submitted successfully with id: ' + str(new_ad_id)
        else:
            return 'your advertisement was not submitted :('


@app.errorhandler(404)
def input_not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(HTTPException)
def handle_exception(e):
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    app.run()
