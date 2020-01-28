import pickle

from googleapiclient.discovery import build
from google.auth.transport.requests import Request

from excel_populator import BASE_DIR, SPREADSHEET_CONF

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def service_builder():
    with open(BASE_DIR + "/token.pickle", "rb") as token:
        creds = pickle.load(token)
        creds.refresh(Request())
    return build("sheets", "v4", credentials=creds)


def write_values(values):
    service = service_builder()
    body = {"values": values}

    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=SPREADSHEET_CONF["spreadsheet_id"],
            range=SPREADSHEET_CONF["range_name"],
            valueInputOption="RAW",
            body=body,
        )
        .execute()
    )

    print(
        "{0} cells appended".format(result.get("updates").get("updatedCells"))
    )
