from flask import Flask, jsonify, render_template, request
from google.cloud import storage
import logging

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        try:
            file = request.files["file"]
            if file:
                client = storage.Client()
                bucket = client.bucket("your-bucket-name")  # replace with your bucket name
                blob = bucket.blob(file.filename)
                blob.upload_from_file(file)
                return f"✅ File '{file.filename}' uploaded to GCS."
            else:
                return "❌ No file found in the request.", 400
        except Exception as e:
            logging.exception("Error during file upload")
            return f"Internal Server Error: {str(e)}", 500
    return render_template("upload.html")
