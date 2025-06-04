# 🌐 GCP POC: Flask Hello World + File Upload to Cloud Storage

This is a simple GCP-based proof of concept project demonstrating:

1. A basic Flask app with UI and API
2. File upload functionality to Google Cloud Storage
3. Deployment to Google App Engine (Standard)

---

## 📁 Project Structure
.
├── app.py # Main Flask application
.
├── app.yaml # GCP deployment config
.
├── requirements.txt # Python dependencies
.
├── .gitignore # Files to ignore in Git
.
├── templates/
.
│ ├── index.html # Homepage (calls Hello API)
.
│ └── upload.html # File upload form
.
├── your-service-key.json # Service account key (do NOT push to GitHub)


---

## 🚀 Features

### `/`
- Displays a webpage and fetches a greeting from `/api/hello`

### `/api/hello`
- Returns a JSON: `{ "message": "Hello, World!" }`

### `/upload`
- Upload a file to your GCS bucket using a simple form

---

## 🛠️ Setup Instructions

### 1. Create and Activate Virtual Environment

```bash
python -m venv temp
source temp/bin/activate  # or temp\Scripts\activate on Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up Google Cloud Credentials
 - Place your service account key in the root directory
 - Update this in app.py:

```bash
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your-service-key.json"
```

 - Also update the bucket name:

```bash
bucket = client.bucket("your-bucket-name")
```

---

## 🌩️ Deploying to Google App Engine

### 1. Deploy with:
```bash
gcloud app deploy
```
Make sure you’re in the correct project and region.

### 2. Open App in Browser:
```bash
gcloud app browse
```

---

## 🔁 Updating Your App on GCP

### Make your changes, and re-deploy with:

```bash
gcloud app deploy
```
GCP will automatically create a new version.