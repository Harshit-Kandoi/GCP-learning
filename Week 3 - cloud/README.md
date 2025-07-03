# 📦 GCP Emulator Project: Pub/Sub + Firestore + Flask Dashboard

This project simulates a full Google Cloud workflow **locally** using emulators — no billing, no GCP credentials.

---

## 🔥 Use Case

> ✅ When a file is uploaded (simulated via message), its metadata is pushed to a **Pub/Sub topic**.  
> 🔁 A subscriber **pulls the message**, extracts metadata, and stores it in **Firestore emulator**.  
> 📊 A **Flask web dashboard** shows all uploaded file info stored in Firestore.

---

## 📁 Folder Structure

cloud/
│
├── main.py # Flask app with / (POST trigger) and /dashboard (GET view)
├── publish.py # Publishes file metadata messages to topic
├── pull_manual.py # Pulls message manually and saves to Firestore
├── setup_pubsub_clean.py # Creates topic & subscription

yaml
Copy
Edit

---

## 🧩 Requirements

- Python ≥ 3.8  
- Firebase CLI  
- Google Cloud SDK  
- VS Code / Terminal  
- Installed libraries:
  ```bash
  pip install flask google-cloud-firestore google-cloud-pubsub
🚀 Step-by-Step Setup
1️⃣ Start Emulators in 3 Terminals
Terminal 1 – Firestore
bash
Copy
Edit
gcloud beta emulators firestore start --host-port=localhost:8080
Terminal 2 – Pub/Sub
bash
Copy
Edit
gcloud beta emulators pubsub start --host-port=localhost:8085
Terminal 3 – Environment Variables
powershell
Copy
Edit
$env:PUBSUB_EMULATOR_HOST = "localhost:8085"
$env:FIRESTORE_EMULATOR_HOST = "localhost:8080"
$env:GOOGLE_CLOUD_PROJECT = "my-local-project"
2️⃣ Setup Topic & Subscription
bash
Copy
Edit
python setup_pubsub_clean.py
3️⃣ Publish a Test File Upload Message
bash
Copy
Edit
python publish.py
4️⃣ Pull Message from Pub/Sub and Save to Firestore
bash
Copy
Edit
python pull_manual.py
5️⃣ Run Flask App (for Dashboard)
bash
Copy
Edit
python main.py
Then open in browser:
👉 http://localhost:5000/dashboard

✅ Output Preview
File Name	Content Type	Created On	File URL
test.txt	text/plain	2025-07-02T16:40:00Z	https://storage.googleapis.com/demo-bucket/...

📌 Notes
You can repeat steps 3 and 4 to simulate multiple file uploads.

pull_manual.py can be extended into a background service or scheduler.

This project does not use real GCP resources — it’s fully local.

🙌 Credits
Developed by Harshit Kandoi
For any guidance or reuse, feel free to connect!