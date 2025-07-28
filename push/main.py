from flask import Flask, request, jsonify
from PIL import Image
import io
from display.interface import show_image

app = Flask(__name__)


@app.route("/")
def index():
    return "Image upload and processing server is running."


@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image part"}), 400

    image_file = request.files["image"]
    if image_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read file into PIL Image
        image_bytes = image_file.read()
        image = Image.open(io.BytesIO(image_bytes))
        image.load()  # Ensure it’s loaded into memory

        # Optional: do something with the image, e.g., get its size
        width, height = image.size
        mode = image.mode
        format = image.format

        show_image(image)

        return jsonify(
            {
                "message": "Image received and processed.",
                "filename": image_file.filename,
                "width": width,
                "height": height,
                "mode": mode,
                "format": format,
            }
        ), 200

    except Exception as e:
        return jsonify({"error": f"Failed to process image: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
