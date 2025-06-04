from flask import Flask, jsonify, render_template, request
from google.cloud import storage
import os

app = Flask(__name__)


# Set service account key path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your-key-file.json"

# Home API route
@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello, World!"})

# Web route
@app.route("/")
def home():
    return render_template("index.html")

# Upload file to GCS
@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            client = storage.Client()
            bucket = client.bucket("your-bucket-name")  # 🔁 replace with your bucket
            blob = bucket.blob(file.filename)
            blob.upload_from_file(file)
            return f"✅ File '{file.filename}' uploaded to GCS."
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
