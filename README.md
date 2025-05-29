# 🚀 Flask Hello World App - Google Cloud Deployment

A simple Flask application that displays a greeting message, deployed on **Google Cloud Platform (GCP)** using **App Engine**.

## 🧩 Features

- REST API endpoint at `/api/hello`
- HTML frontend displaying fetched message
- Deployment-ready for GCP App Engine
- Auto-scaling enabled with minimal configuration

## 🏗️ Folder Structure
├── app.py

├── app.yaml

├── requirements.txt

├── templates/

│ └── index.html

├── Dockerfile

├── .dockerignore

├── .gitignore

├── .gcloudignore

└── README.md

## 🔧 How to Run Locally

### Option 1: Using Flask directly
```bash
# Create virtual environment
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```
Visit http://localhost:5000 in your browser.

### Option 2: Using Docker
```bash
docker build -t hello .
docker run -p 8080:8080 hello
```
Visit http://localhost:8080

## ☁️ Deploying to Google Cloud

- Install and initialize the Google Cloud SDK
- Authenticate and set the project:
```bash
gcloud init
```
- Deploy:
```bash
gcloud app deploy
```
- Open in browser:
```bash
gcloud app browse
```
