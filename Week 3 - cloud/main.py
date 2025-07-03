from flask import Flask, request, render_template_string
from google.cloud import firestore
import base64
import json
import os

app = Flask(__name__)
db = firestore.Client(project=os.environ["GOOGLE_CLOUD_PROJECT"])

@app.route("/", methods=["POST"])
def pubsub_trigger():
    envelope = request.get_json()
    if not envelope or 'message' not in envelope:
        return 'Bad Request', 400

    data = envelope['message'].get('data')
    if data:
        decoded = base64.b64decode(data).decode("utf-8")
        msg = json.loads(decoded)

        metadata = {
            'bucket': msg.get('bucket'),
            'name': msg.get('name'),
            'content_type': msg.get('contentType', 'unknown'),
            'size': msg.get('size', 0),
            'created_on': msg.get('timeCreated'),
            'file_url': f"https://storage.googleapis.com/{msg.get('bucket')}/{msg.get('name')}"
        }
        db.collection("uploaded_files").add(metadata)
        print("✅ Metadata Saved:", metadata)

    return "OK", 200

@app.route("/dashboard", methods=["GET"])
def dashboard():
    docs = db.collection("uploaded_files").stream()
    files = [doc.to_dict() for doc in docs]

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Uploaded Files Dashboard</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
            th { background-color: #f2f2f2; }
            h2 { display: flex; align-items: center; gap: 10px; }
        </style>
    </head>
    <body>
        <h2>📦 Uploaded Files Metadata</h2>
        <table>
            <tr>
                <th>File Name</th>
                <th>Bucket</th>
                <th>Content Type</th>
                <th>Size (bytes)</th>
                <th>Uploaded At</th>
                <th>File URL</th>
            </tr>
            {% for f in files %}
            <tr>
                <td>{{ f.name }}</td>
                <td>{{ f.bucket }}</td>
                <td>{{ f.content_type }}</td>
                <td>{{ f.size }}</td>
                <td>{{ f.created_on }}</td>
                <td><a href="{{ f.file_url }}" target="_blank">View</a></td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, files=files)

if __name__ == "__main__":
    app.run(port=5000)
