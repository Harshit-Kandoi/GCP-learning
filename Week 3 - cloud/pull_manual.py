import json
import os
from google.cloud import pubsub_v1, firestore
from google.api_core.client_options import ClientOptions

# Emulator config
project_id = "my-local-project"
sub_id = "file-upload-sub"
subscription_path = f"projects/{project_id}/subscriptions/{sub_id}"
emulator_host = os.getenv("PUBSUB_EMULATOR_HOST", "localhost:8085")

# ✅ SET FIRESTORE EMULATOR HOST
os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"

# Pub/Sub client with emulator
client_options = ClientOptions(api_endpoint=emulator_host)
subscriber = pubsub_v1.SubscriberClient(client_options=client_options)

# ✅ Firestore emulator client — now works without credentials
db = firestore.Client(project=project_id)

print("📥 Pulling messages manually...")

response = subscriber.pull(
    request={"subscription": subscription_path, "max_messages": 5},
    timeout=5
)

if not response.received_messages:
    print("⚠️ No messages found.")
else:
    for msg in response.received_messages:
        decoded = msg.message.data.decode("utf-8")
        print("📩 Message pulled:", decoded)
        json_data = json.loads(decoded)
        metadata = {
            "bucket": json_data.get("bucket"),
            "name": json_data.get("name"),
            "content_type": json_data.get("contentType", "unknown"),
            "created_on": json_data.get("timeCreated"),
            "file_url": f"https://storage.googleapis.com/{json_data.get('bucket')}/{json_data.get('name')}"
        }
        db.collection("uploaded_files").add(metadata)
        print("✅ Metadata saved:", metadata)

        subscriber.acknowledge(
            request={
                "subscription": subscription_path,
                "ack_ids": [msg.ack_id]
            }
        )
        print("✅ Message acknowledged.")