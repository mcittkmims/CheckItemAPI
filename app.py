import os
import base64
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from nsfw_checker import nsfw_image_checker, nsfw_text_checker
from get_image import fetch_image

# Initialize the Flask app
app = Flask(__name__)

load_dotenv()


@app.route('/check', methods=['POST'])
def check_image_and_text():
    data = request.get_json()

    # Extract image_url, image_content, and description text
    image_url = data.get('image_url')
    image_content = data.get('image_content')
    description = data.get('description')

    # Validate the input data: Both 'image_content' and 'description' must be provided
    if not description:
        return jsonify({
            "error": "Bad Request",
            "message": "'description' is required",
            "code": 400
        }), 400

    if not (image_url or image_content):
        return jsonify({
            "error": "Bad Request",
            "message": "Either 'image_url' or 'image_content' must be provided",
            "code": 400
        }), 400

    # If image_url is provided, fetch the image content
    if image_url:
        try:
            image_content = fetch_image(image_url)  # Assuming fetch_image is implemented elsewhere
        except ValueError as e:
            return jsonify({
                "error": "Not Found",
                "message": f"Failed to fetch image from URL: {str(e)}",
                "code": 404
            }), 404
    elif isinstance(image_content, str):  # Ensure image_content is base64-encoded
        try:
            image_content = base64.b64decode(image_content)
        except Exception as e:
            return jsonify({
                "error": "Bad Request",
                "message": f"Invalid base64-encoded image content: {str(e)}",
                "code": 400
            }), 400

    # Perform NSFW check on the image
    try:
        image_result = nsfw_image_checker(image_content, os.getenv('CONTENT_SAFETY_ENDPOINT'), os.getenv('CONTENT_SAFETY_KEY'))
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": f"An error occurred while processing the image: {str(e)}",
            "code": 500
        }), 500

    # Perform NSFW check on the description text
    try:
        text_result = nsfw_text_checker(description, os.getenv('CONTENT_SAFETY_ENDPOINT'), os.getenv('CONTENT_SAFETY_KEY'))
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": f"An error occurred while analyzing the text: {str(e)}",
            "code": 500
        }), 500

    # Combine the results and return them
    return jsonify({
        "image_check": image_result,
        "text_check": text_result
    })


if __name__ == '__main__':
    app.run()