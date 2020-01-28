import pickle
import os

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1bUjYYZl9vQUTijneavY2QmhxlpjFvP0j5G8YhEgTSQo"


def service_builder():
    with open("token.pickle", "rb") as token:
        creds = pickle.load(token)
        creds.refresh(Request())
    return build("sheets", "v4", credentials=creds)
