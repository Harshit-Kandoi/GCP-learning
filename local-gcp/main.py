from flask import Flask, request, redirect, render_template_string, url_for
from flask import send_from_directory
from google.cloud import firestore
import os
import threading
import time
import json
import google.auth.credentials
from google.cloud import pubsub_v1
from google.api_core.client_options import ClientOptions

# Emulator env setup
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "my-local-project")
os.environ.setdefault("FIRESTORE_EMULATOR_HOST", "localhost:8080")
os.environ.setdefault("PUBSUB_EMULATOR_HOST", "localhost:8085")

app = Flask(__name__)
app.config["SERVER_NAME"] = "localhost:5000"
UPLOAD_FOLDER = "local_bucket"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Firestore client using emulator
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-local-project")
credentials = google.auth.credentials.AnonymousCredentials()
db = firestore.Client(project=project_id, credentials=credentials)

# PubSub config
subscriber = pubsub_v1.SubscriberClient(
    client_options=ClientOptions(api_endpoint=os.environ["PUBSUB_EMULATOR_HOST"]),
    credentials=credentials,
)
subscription_path = f"projects/{project_id}/subscriptions/file-upload-sub"


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            print(f"✅ File uploaded: {filepath}")
            # NOTE: no redirect, just return a message
            return "✅ File uploaded. Now <a href='/dashboard'>Go to Dashboard</a>"
    return render_template_string("""
        <h2>📤 Upload File to Local Bucket</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <input type="submit" value="Upload">
        </form>
        <a href="{{ url_for('dashboard') }}">📊 View Uploaded Logs</a>
    """)


@app.route("/dashboard")
def dashboard():
    docs = db.collection("uploaded_files").stream()
    rows = []
    for doc in docs:
        info = doc.to_dict()
        file_path = os.path.join(UPLOAD_FOLDER, info.get("name"))
        info["file_exists"] = os.path.exists(file_path)
        info["file_url"] = url_for("serve_file", filename=info.get("name")) if info["file_exists"] else "#"
        rows.append({
            "file_name": info.get("name"),
            "bucket": info.get("bucket"),
            "type": info.get("content_type"),
            "size": info.get("size", "-"),
            "url": info["file_url"],
            "created": info.get("created_on"),
            "exists": info["file_exists"]
        })

    return render_template_string("""
        <h2>📦 Uploaded Files Metadata</h2>
        <table border="1" cellpadding="10">
            <tr><th>File Name</th><th>Bucket</th><th>Content Type</th><th>Size</th><th>Uploaded At</th><th>File URL</th></tr>
            {% for row in rows %}
            <tr>
                <td>{{ row.file_name }}</td>
                <td>{{ row.bucket }}</td>
                <td>{{ row.type }}</td>
                <td>{{ row.size }}</td>
                <td>{{ row.created }}</td>
                <td>
                    {% if row.exists %}
                        <a href="{{ row.url }}" target="_blank">View</a>
                    {% else %}
                        ❌ Deleted
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </table>
        <br>
        <a href="{{ url_for('upload_file') }}">⬅️ Back to Upload</a>
    """, rows=rows)

@app.route('/files/<path:filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# 🔁 Background process: Pull messages and save metadata
def run_pubsub_listener():
    print("🔄 Pub/Sub listener started...")
    while True:
        response = subscriber.pull(
            request={"subscription": subscription_path, "max_messages": 5},
            timeout=3,
        )
        if not response.received_messages:
            time.sleep(2)
            continue

        for msg in response.received_messages:
            decoded = msg.message.data.decode("utf-8")
            print("📩 Received message:", decoded)
            data = json.loads(decoded)

            with app.app_context():
                metadata = {
                    "bucket": data.get("bucket"),
                    "name": data.get("name"),
                    "content_type": data.get("contentType", "unknown"),
                    "created_on": data.get("timeCreated"),
                    "size": data.get("size", "-"),
                    "file_url": url_for("serve_file", filename=data.get("name"), _external=True)
                }
                db.collection("uploaded_files").add(metadata)
                print("✅ Saved metadata to Firestore:", metadata)

                subscriber.acknowledge(
                    request={"subscription": subscription_path, "ack_ids": [msg.ack_id]}
                )



# 👀 Background watcher that simulates your watcher.py
def watch_upload_folder():
    print("👀 Watching folder for new files...")
    known = set(os.listdir(UPLOAD_FOLDER))
    publisher = pubsub_v1.PublisherClient()
    topic_path = f"projects/{project_id}/topics/file-upload-topic"

    while True:
        current = set(os.listdir(UPLOAD_FOLDER))
        new_files = current - known
        for file_name in new_files:
            file_path = os.path.join(UPLOAD_FOLDER, file_name)
            message = {
                "bucket": "local_bucket",
                "name": file_name,
                "contentType": "image/jpeg",
                "timeCreated": time.strftime("%Y-%m-%d %H:%M:%S"),
                "size": os.path.getsize(file_path)
            }
            publisher.publish(topic_path, data=json.dumps(message).encode("utf-8"))
            print(f"📤 Published new file: {file_name}")
        known = current
        time.sleep(2)


if __name__ == "__main__":
    # Run pubsub + watcher in background threads
    threading.Thread(target=run_pubsub_listener, daemon=True).start()
    threading.Thread(target=watch_upload_folder, daemon=True).start()
    # Run Flask server
    app.run(debug=True, port=5000)
