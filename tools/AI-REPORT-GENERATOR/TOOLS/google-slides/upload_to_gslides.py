#!/usr/bin/env python3
"""
Google Slides Integration Tool (TOOLS/google-slides/upload_to_gslides.py).
Uploads local 16:9 .pptx presentations to Google Slides via Google Drive API (if credentials exist),
or launches one-click browser upload helper.
"""

import sys
import os
import subprocess

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.oauth2 import service_account, credentials
except ImportError:
    build = None


def upload_pptx_to_google_slides(pptx_path: str, creds_path: str = None) -> str:
    """Uploads PPTX file to Google Drive and converts it into native Google Slides presentation."""
    if not os.path.exists(pptx_path):
        raise FileNotFoundError(f"File not found: {pptx_path}")

    # 1. Check if Google Drive API credentials exist
    if build and creds_path and os.path.exists(creds_path):
        try:
            creds = service_account.Credentials.from_service_account_file(
                creds_path, scopes=['https://www.googleapis.com/auth/drive.file']
            )
            drive_service = build('drive', 'v3', credentials=creds)
            
            file_metadata = {
                'name': os.path.splitext(os.path.basename(pptx_path))[0],
                'mimeType': 'application/vnd.google-apps.presentation'
            }
            media = MediaFileUpload(
                pptx_path,
                mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
                resumable=True
            )
            
            file = drive_service.files().create(
                body=file_metadata, media_body=media, fields='id, webViewLink'
            ).execute()
            
            web_link = file.get('webViewLink')
            print(f"✔ Successfully uploaded to Google Slides API: {web_link}")
            return web_link
        except Exception as e:
            print(f"[WARNING] Google Drive API upload failed: {e}")

    # 2. One-click macOS Browser & Finder Helper
    print("\n------------------------------------------------------------")
    print("🌐 Launching One-Click Google Slides Upload Helper")
    print("------------------------------------------------------------")
    print(f"File to upload: {pptx_path}")
    
    # Reveal file in Finder
    try:
        subprocess.run(["open", "-R", pptx_path])
    except Exception:
        pass

    # Open slides.new in browser
    try:
        subprocess.run(["open", "https://slides.new"])
    except Exception:
        pass

    return "https://slides.new"


if __name__ == "__main__":
    pptx_path = sys.argv[1] if len(sys.argv) > 1 else "/Users/ts-1148/Desktop/Pulu-workspace-v2/AI-REPORT-GENERATOR/OUTPUT/Ahamove_DM_Real_Meeting_Report/real_report_editable.pptx"
    creds_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    link = upload_pptx_to_google_slides(pptx_path, creds_path)
    print(f"\nGoogle Slides Upload Link / Helper: {link}")
