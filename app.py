from flask import Flask, request, jsonify
import requests
import base64
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

GEMINI_API_URL = "test"  # Replace with Gemini’s image analysis endpoint
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/api/analyze-image", methods=["POST"])
def analyze_image():
    try:
        # Check for image file or URL
        if "image" in request.files:
            image_data = base64.b64encode(request.files["image"].read()).decode("utf-8")
        elif request.json and "imageUrl" in request.json:
            image_data = request.json["imageUrl"]
        else:
            return jsonify({"success": False, "error": "No image file or URL provided"}), 400

        # Send to Gemini API
        headers = {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            GEMINI_API_URL,
            json={"image": image_data},  # Adjust based on Gemini’s API requirements
            headers=headers
        )
        response.raise_for_status()

        return jsonify({"success": True, "result": response.json()}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "API is running"}), 200

if __name__ == "__main__":
    app.run()
