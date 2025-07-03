import requests
import json
import base64

def test_notification_endpoint():
    """Test if the notification endpoint is accessible"""
    
    # Your App Engine URL
    app_url = "https://training-461208.appspot.com"
    
    # Test 1: Check if app is accessible
    try:
        response = requests.get(f"{app_url}/")
        print(f"✅ App is accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ App not accessible: {str(e)}")
        return
    
    # Test 2: Test notification endpoint with sample data
    sample_data = {
        "bucketId": "training-461208.appspot.com",
        "name": "test-file.txt",
        "eventType": "OBJECT_FINALIZE",
        "timeCreated": "2024-01-01T00:00:00.000Z"
    }
    
    pubsub_message = {
        "message": {
            "data": base64.b64encode(json.dumps(sample_data).encode()).decode()
        }
    }
    
    try:
        response = requests.post(
            f"{app_url}/notification",
            json=pubsub_message,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"✅ Notification endpoint response: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"❌ Notification endpoint error: {str(e)}")

if __name__ == "__main__":
    print("Testing your App Engine notification endpoint...")
    test_notification_endpoint() 