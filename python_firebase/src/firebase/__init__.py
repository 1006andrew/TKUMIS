# firebase/init_firebase.py
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("C:/Users/ABC/Desktop/code2/python_firebase_project_20250826_151644/serviceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)
