"""
Upload weekly-ops-dashboard.xlsx to Google Drive as a Google Spreadsheet.
First run: opens browser for Google auth → saves token.json for future runs.
"""
import os, json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/drive.file']
FILE_PATH = os.path.join(os.path.dirname(__file__),
    'output/Ahamove/04. OPS_METRICS/weekly-ops-dashboard.xlsx')
TITLE = 'Ahamove Weekly Ops Dashboard'
TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'token.json')
CREDS_FILE = os.path.join(os.path.dirname(__file__), 'google_credentials.json')

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDS_FILE):
                print("\n❌  Chưa có file credentials.")
                print("    1. Vào: https://console.cloud.google.com/apis/credentials")
                print("    2. Create Credentials → OAuth 2.0 Client IDs → Desktop App")
                print(f"    3. Download JSON → đặt tên 'google_credentials.json' vào: {os.path.dirname(__file__)}")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
    return creds

def upload():
    creds = get_credentials()
    if not creds:
        return

    service = build('drive', 'v3', credentials=creds)

    media = MediaFileUpload(
        FILE_PATH,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        resumable=True
    )
    meta = {
        'name': TITLE,
        'mimeType': 'application/vnd.google-apps.spreadsheet'  # convert to Sheets
    }

    print(f"Uploading '{TITLE}'...")
    result = service.files().create(
        body=meta, media_body=media, fields='id,name,webViewLink'
    ).execute()

    print(f"\n✅  Uploaded successfully!")
    print(f"    Name : {result['name']}")
    print(f"    ID   : {result['id']}")
    print(f"    Link : {result['webViewLink']}")
    return result

if __name__ == '__main__':
    upload()
