from google.cloud import pubsub_v1
import os

os.environ["PUBSUB_EMULATOR_HOST"] = "localhost:8085"
os.environ["GOOGLE_CLOUD_PROJECT"] = "my-local-project"

project_id = "my-local-project"
topic_id = "file-upload-topic"
sub_id = "file-upload-sub"

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

topic_path = publisher.topic_path(project_id, topic_id)
sub_path = subscriber.subscription_path(project_id, sub_id)

# ✅ Create topic if not exists
try:
    publisher.create_topic(request={"name": topic_path})
    print(f"✅ Created topic: {topic_path}")
except Exception as e:
    print(f"⚠️ Topic may already exist: {e}")

# ✅ Create subscription if not exists
try:
    subscriber.create_subscription(
        request={
            "name": sub_path,
            "topic": topic_path
        }
    )
    print(f"✅ Created subscription: {sub_path}")
except Exception as e:
    print(f"⚠️ Subscription may already exist: {e}")
