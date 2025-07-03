from flask import Flask, request, render_template, jsonify
from google.cloud import storage, firestore, pubsub_v1
from datetime import datetime
import json
import base64

app = Flask(__name__)

# Initialize GCP clients
storage_client = storage.Client()
firestore_client = firestore.Client(project='training')  # replace with actual project ID

# Your bucket name
BUCKET_NAME = 'training-461208.appspot.com'  # replace with actual

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/hello")
def hello_api():
    return {"message": "Hello, World!"}

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files['file']
        if file:
            bucket = storage_client.bucket(BUCKET_NAME)
            blob = bucket.blob(file.filename)
            blob.upload_from_file(file, content_type=file.content_type)

             # Refresh metadata from GCS
            blob.reload()
            
            # Create Firestore doc
            doc_ref = firestore_client.collection("file_metadata").document()
            doc_ref.set({
                "id": doc_ref.id,
                "file_name": file.filename,
                "upload_on": firestore.SERVER_TIMESTAMP,
                "upload_path": f"gs://{BUCKET_NAME}/{file.filename}",
                "content_type": file.content_type,
            })

            return f"✅ File '{file.filename}' uploaded successfully!"

    return render_template("upload.html")

@app.route("/notification", methods=["POST"])
def notification():
    """Handle Pub/Sub push notifications from Cloud Storage - Optimized Version"""
    try:
        # Get the request data
        envelope = request.get_json()
        
        if not envelope:
            print("❌ No Pub/Sub message received")
            return jsonify({"error": "No Pub/Sub message received"}), 400

        if not isinstance(envelope, dict) or "message" not in envelope:
            print("❌ Invalid Pub/Sub message format")
            return jsonify({"error": "Invalid Pub/Sub message format"}), 400

        # Extract the Pub/Sub message
        pubsub_message = envelope["message"]
        
        if isinstance(pubsub_message, dict) and "data" in pubsub_message:
            # Decode the data
            data = base64.b64decode(pubsub_message["data"]).decode("utf-8")
            notification_data = json.loads(data)
            
            # Extract relevant information from the notification
            bucket_id = notification_data.get("bucketId", "")
            object_id = notification_data.get("name", "")
            event_type = notification_data.get("eventType", "")
            event_time = notification_data.get("timeCreated", "")
            
            # Only process specific events (optional filtering)
            if event_type in ["OBJECT_FINALIZE", "OBJECT_DELETE", "OBJECT_ARCHIVE"]:
                # Save notification data to Firestore with optimized structure
                doc_ref = firestore_client.collection("file_events").document()
                doc_ref.set({
                    "id": doc_ref.id,
                    "bucket_id": bucket_id,
                    "object_id": object_id,
                    "event_type": event_type,
                    "event_time": event_time,
                    "notification_received_at": firestore.SERVER_TIMESTAMP,
                    "file_size": notification_data.get("size", 0),
                    "content_type": notification_data.get("contentType", ""),
                    "generation": notification_data.get("generation", ""),
                    "metageneration": notification_data.get("metageneration", ""),
                    "raw_notification": notification_data
                })
                
                print(f"✅ Event saved: {event_type} for {object_id} in {bucket_id}")
                return jsonify({"status": "success", "message": "Event processed and saved"}), 200
            else:
                print(f"⚠️ Skipping event type: {event_type}")
                return jsonify({"status": "skipped", "message": f"Event type {event_type} not processed"}), 200
        else:
            print("❌ Invalid message data structure")
            return jsonify({"error": "Invalid message data"}), 400
            
    except Exception as e:
        print(f"❌ Error processing notification: {str(e)}")
        return jsonify({"error": f"Error processing notification: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
