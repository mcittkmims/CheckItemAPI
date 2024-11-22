import os
import base64
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from nsfw_checker import nsfw_image_checker
from get_image import fetch_image

# Initialize the Flask app
app = Flask(__name__)

load_dotenv()


@app.route('/check', methods=['POST'])
def check_image():

    data = request.get_json()

    # Extract image_url, image_content, and description text
    image_url = data.get('image_url')
    image_content = data.get('image_content')
    description = data.get('description')

    # Validate the input data
    if not description:
        return jsonify({
            "error": "Not Found",
            "message": "'description' is required",
            "code": 404
        }), 404

    # Check if either image_url or image_content is provided
    if image_url:
        # Fetch the image content from the URL (using the fetch_image function)
        try:
            image_content = fetch_image(image_url)
        except ValueError as e:
            # If fetching the image fails, return a JSON response with error message
            return jsonify({
                "error": "Not Found",
                "message": f"Failed to fetch image from URL: {str(e)}",
                "code": 404
            }), 404
    elif not image_content:
        return jsonify({
            "error": "Bad Request",
            "message": "Either 'image_url' or 'image_content' must be provided",
            "code": 400
        }), 400

    # If image_content is base64-encoded, decode it
    if isinstance(image_content, str):
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
        result = nsfw_image_checker(image_content, os.getenv('CONTENT_SAFETY_ENDPOINT'), os.getenv('CONTENT_SAFETY_KEY'))
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": f"An error occurred while processing the image: {str(e)}",
            "code": 500
        }), 500

    # Return the result as a JSON response
    return jsonify(result), result["code"]


if __name__ == '__main__':
    app.run()