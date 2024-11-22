from flask import Flask, jsonify
from dotenv import load_dotenv

# Initialize the Flask app
app = Flask(__name__)

load_dotenv()
# Define a simple route
@app.route('/check', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"})

# Run the app
if __name__ == '__main__':
    app.run()
