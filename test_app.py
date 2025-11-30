import requests
import json
import random
import string

# Configuration
BASE_URL = "http://localhost:8000"  # Django Backend (internal to container is localhost since we run it there)
NOTIFICATION_SERVICE_URL = "http://notification-service:8000" # Notification Service (docker DNS)

def generate_random_email():
    return f"testuser_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}@example.com"

def test_notification_service_direct():
    print("\n--- Testing Notification Service Directly ---")
    payload = {
        "email": "test_direct@example.com",
        "subject": "Direct Test",
        "message": "This is a direct test of the notification service."
    }
    try:
        response = requests.post(f"{NOTIFICATION_SERVICE_URL}/send-email/", json=payload)
        if response.status_code == 200:
            print("✅ Notification Service is reachable and accepted the request.")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Notification Service failed with status {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Could not connect to Notification Service: {e}")

def test_full_registration_flow():
    print("\n--- Testing Full Registration Flow (Django -> Notification) ---")
    email = generate_random_email()
    password = "password123"
    
    payload = {
        "email": email,
        "password": password,
        "first_name": "Test",
        "last_name": "User",
        "dni": "12345678",
        "phone": "987654321"
    }
    
    print(f"Attempting to register user: {email}")
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register/", json=payload)
        
        if response.status_code == 201:
            print("✅ User registered successfully in Django.")
            print("👉 Now check your Brevo/Email logs or inbox to see if the email was sent.")
        else:
            print(f"❌ Registration failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Could not connect to Django Backend: {e}")

if __name__ == "__main__":
    test_notification_service_direct()
    test_full_registration_flow()
