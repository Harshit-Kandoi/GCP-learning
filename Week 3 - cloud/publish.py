import json
import os
from google.cloud import pubsub_v1
from google.api_core.client_options import ClientOptions

# Emulator configuration
project_id = "my-local-project"
topic_id = "file-upload-topic"
topic_path = f"projects/{project_id}/topics/{topic_id}"
emulator_host = os.getenv("PUBSUB_EMULATOR_HOST", "localhost:8085")

# Explicitly use emulator endpoint
client_options = ClientOptions(api_endpoint=emulator_host)
publisher = pubsub_v1.PublisherClient(client_options=client_options)

# Message
message_json = json.dumps({
    "bucket": "demo-bucket",
    "name": "test.txt",
    "contentType": "text/plain",
    "size": 4,
    "timeCreated": "2025-07-02T16:40:00Z"
})
message_bytes = message_json.encode("utf-8")

future = publisher.publish(topic_path, message_bytes)
print("📤 Message sent to topic.")
try:
    message_id = future.result()
    print(f"✅ Message published with ID: {message_id}")
except Exception as e:
    print(f"❌ Error publishing message: {e}")