import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from datetime import datetime, timezone

json_file_path = 'upload_video.py-oauth2.json'

with open(json_file_path, 'r') as file:
    credentials_data = json.load(file)

if 'token_expiry' in credentials_data:
    credentials_data['token_expiry'] = datetime.fromisoformat(
        credentials_data['token_expiry'].replace('Z', '+00:00')
    ).replace(tzinfo=None)

creds = Credentials(
    token=credentials_data['access_token'],
    refresh_token=credentials_data['refresh_token'],
    token_uri=credentials_data['token_uri'],
    client_id=credentials_data['client_id'],
    client_secret=credentials_data['client_secret'],
    scopes=credentials_data['scopes'],
    expiry=credentials_data.get('token_expiry')
)

print(f"Token expiry: {creds.expiry} (naive datetime)")
print(f"Current time: {datetime.now()} (naive datetime)")

if creds.expired and creds.refresh_token:
    print("Token is expired, refreshing...")
    creds.refresh(Request())
    print("Access token refreshed.")

    credentials_data['access_token'] = creds.token
    credentials_data['token_expiry'] = creds.expiry.isoformat() if creds.expiry else None

    with open(json_file_path, 'w') as file:
        json.dump(credentials_data, file, indent=4)
else:
    print("Access token is still valid.")
