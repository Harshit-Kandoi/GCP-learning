
# 📦 Local GCP Emulator: File Upload & Metadata Viewer

This project simulates a **Google Cloud Platform (GCP)** workflow entirely **locally** using emulators for **Firestore** and **Pub/Sub**.

It allows users to:

- Upload files to a local folder (`local_bucket`)
- Automatically detect and publish file metadata to a local Pub/Sub topic
- Pull the messages and save metadata into Firestore (via emulator)
- View uploaded file metadata on a Flask dashboard
- Access uploaded files through direct file links

---

## 🚀 Features

- 📤 Upload files via a Flask web interface  
- 📡 Auto-detect file uploads and send metadata using **Pub/Sub Emulator**  
- 🧠 Consume messages and store metadata in **Firestore Emulator**  
- 🖼️ View all uploaded file data including:
  - File name
  - Type
  - Size
  - Upload time
  - File URL (served locally)

---

## 📁 Project Structure

```
local-gcp/
├── main.py               # Main Flask app with integrated watcher & listener
├── setup_pubsub_clean.py # Script to create Pub/Sub topic & subscription
├── requirements.txt      # Python dependencies
├── local_bucket/         # Simulated GCS bucket (locally stored files)
└── README.md             # (You're here!)
```

---

## ⚙️ Setup Instructions

### ✅ Prerequisites

- Python 3.8+  
- Google Cloud SDK installed locally: [Install Guide](https://cloud.google.com/sdk/docs/install)

### 📦 Install Python Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt** should contain:

```
flask
google-cloud-pubsub
google-cloud-firestore
```

---

## 🔥 Start GCP Emulators

> Start each in a separate terminal

### Firestore Emulator

```bash
gcloud beta emulators firestore start --host-port=localhost:8080
```

### Pub/Sub Emulator

```bash
gcloud beta emulators pubsub start --host-port=localhost:8085
```

---

## 🧪 Set Environment Variables

Before running `main.py`:

### On Linux/macOS

```bash
export GOOGLE_CLOUD_PROJECT=my-local-project
export FIRESTORE_EMULATOR_HOST=localhost:8080
export PUBSUB_EMULATOR_HOST=localhost:8085
```

### On Windows CMD

```cmd
set GOOGLE_CLOUD_PROJECT=my-local-project
set FIRESTORE_EMULATOR_HOST=localhost:8080
set PUBSUB_EMULATOR_HOST=localhost:8085
```

---

## 🔁 Setup Pub/Sub Topic & Subscription

After starting the Pub/Sub emulator, run this one-time setup:

```bash
python setup_pubsub_clean.py
```

This script creates the topic `file-upload-topic` and the subscription `file-upload-sub`.

---

## ▶️ Run the Flask App

```bash
python main.py
```

This will:

- Start Flask at `http://127.0.0.1:5000/`
- Run two background threads:
  - 👀 Watching new files in `local_bucket/`
  - 🔁 Listening to Pub/Sub messages

---

## 🧠 How It Works

1. You upload a file through the web UI.
2. It's saved in `local_bucket/`
3. A background thread detects the new file and publishes metadata to Pub/Sub.
4. Another thread listens to Pub/Sub and saves metadata to Firestore.
5. The `/dashboard` route shows all file data and gives you a clickable link to access the file.

---

## 🖼️ Sample Dashboard

After uploading a file, visit:

👉 [http://127.0.0.1:5000/dashboard](http://127.0.0.1:5000/dashboard)

You'll see a list of files like:

| File Name | Type | Size | Uploaded At | URL |
|-----------|------|------|-------------|-----|

---

## 📌 Notes

- This project uses Google Emulator Services – no internet or billing is required.
- Uploaded files stay in `local_bucket/`.
- Deleting files from the folder does **not** delete metadata from Firestore.
- You can create an optional `cleanup.py` script to sync deletions.

---

## ✅ Final Flow Order

1. Start Firestore emulator  
2. Start Pub/Sub emulator  
3. Set environment variables  
4. Run `setup_pubsub_clean.py`
5. Run `main.py`

---

## 📧 Contact

**Made with ❤️ by Harshit Kandoi**  
Reach out if you need help customizing this setup for cloud deployment.
