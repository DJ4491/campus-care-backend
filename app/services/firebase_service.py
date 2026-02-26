# app/services/firebase_service.py

import os
import json
from dotenv import load_dotenv

# 🔥 Load .env file FIRST
load_dotenv()

import firebase_admin
from firebase_admin import credentials, auth as firebase_auth, firestore


# Option A: credentials file path from env
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if cred_path and os.path.exists(cred_path):
    cred = credentials.Certificate(cred_path)
else:
    # Option B: credentials json content in env
    sa_json = os.getenv("FIREBASE_ADMIN_JSON")
    if not sa_json:
        raise RuntimeError("No Firebase admin credentials found")

    cred = credentials.Certificate(json.loads(sa_json))


# Initialize Firebase app only once
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
    print(f"FIREBASE_SERVICE: Initialized for project: {firebase_admin.get_app().project_id}")
db = firestore.client()
auth = firebase_auth