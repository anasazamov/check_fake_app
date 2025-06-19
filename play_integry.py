import requests
import json

# Replace with your Google Cloud project credentials
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
INTEGRITY_API_URL = f"https://playintegrity.googleapis.com/v1/verifyIntegrity?key={GOOGLE_API_KEY}"

def verify_play_integrity(token):
    """
    Verifies the Play Integrity token using Google's API.
    """
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "integrityToken": token
    }

    try:
        response = requests.post(INTEGRITY_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an error for HTTP issues
        return response.json()  # Parsed JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error verifying token: {e}")
        return None

# Example usage
integrity_token = "YOUR_INTEGRITY_TOKEN_FROM_APP"
result = verify_play_integrity(integrity_token)

if result:
    print("Play Integrity Data:", json.dumps(result, indent=4))
else:
    print("Failed to verify the token.")