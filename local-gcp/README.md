📦 Local GCP Emulator: File Upload & Metadata Viewer
This project simulates a Google Cloud Platform (GCP) workflow entirely locally using emulators for Firestore and Pub/Sub. It allows users to:

Upload files to a local folder (local_bucket)

Automatically detect and publish file metadata to a local Pub/Sub topic

Pull the messages and save metadata into Firestore (via emulator)

View uploaded file metadata on a Flask dashboard

Access uploaded files through direct file links

🚀 Features
📤 Upload files via a Flask web interface

📡 Auto-detect file uploads and send metadata using Pub/Sub Emulator

🧠 Consume messages and store metadata in Firestore Emulator

🖼️ View all uploaded file data including:

File name

Type

Size

Upload time

File URL (served locally)

📁 Project Structure
graphql
Copy
Edit
local-gcp/
│
├── main.py               # Main Flask app with integrated watcher & listener
├── requirements.txt      # Python dependencies
├── local_bucket/         # Simulated GCS bucket (locally stored files)
└── README.md             # (You're here!)
⚙️ Setup Instructions
1. ✅ Prerequisites
Python 3.8+

Google Cloud SDK installed locally:
https://cloud.google.com/sdk/docs/install

2. 📦 Install Python Dependencies
bash
Copy
Edit
pip install -r requirements.txt
Contents of requirements.txt:

nginx
Copy
Edit
flask
google-cloud-pubsub
google-cloud-firestore
3. 🚀 Start GCP Emulators
Start Firestore Emulator:
bash
Copy
Edit
gcloud beta emulators firestore start --host-port=localhost:8080
Start Pub/Sub Emulator:
bash
Copy
Edit
gcloud beta emulators pubsub start --host-port=localhost:8085
In separate terminals.

4. 🧪 Set Environment Variables
Set the emulator environment variables before running main.py:

bash
Copy
Edit
export GOOGLE_CLOUD_PROJECT=my-local-project
export FIRESTORE_EMULATOR_HOST=localhost:8080
export PUBSUB_EMULATOR_HOST=localhost:8085
For Windows CMD:

cmd
Copy
Edit
set GOOGLE_CLOUD_PROJECT=my-local-project
set FIRESTORE_EMULATOR_HOST=localhost:8080
set PUBSUB_EMULATOR_HOST=localhost:8085


5. Setup Pub/Sub Topic & Subscription
After starting the Pub/Sub emulator, run this script to create topic and subscription:

bash
Copy
Edit
python setup_pubsub_clean.py

6. ▶️ Run the Flask App
bash
Copy
Edit
python main.py
This will:

Start Flask at http://127.0.0.1:5000/

Start background threads for:

Watching new files in local_bucket/

Listening to Pub/Sub messages

🧠 How It Works
You upload a file through the web UI.

It’s saved in local_bucket/.

A background thread detects the new file and publishes metadata to Pub/Sub.

Another thread listens to Pub/Sub and saves metadata to Firestore.

The /dashboard route shows all file data and gives you a clickable link to access the file.

🖼️ Sample Dashboard
After upload, visit:
👉 http://127.0.0.1:5000/dashboard

You’ll see a list of files like:

File Name	Type	Size	Uploaded At	URL

📌 Notes
This project uses Google Emulator Services, no internet or billing is required.

Uploaded files stay in local_bucket/, deleting them will only remove access but not delete Firestore metadata.

You can integrate a cleanup.py to sync deletions across local and metadata if required.

Final Flow Order
1. Start Firestore emulator
2. Start Pub/Sub emulator
3. Set environment variables
4. Run setup_pubsub_clean.py ← ✅ This step creates topic & sub
5. Run main.py

📧 Contact
Made with ❤️ by Harshit Kandoi
Reach me if you need help customizing this setup for cloud deployment.