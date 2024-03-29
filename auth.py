import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

tokens = {}

def authorize(user: str) -> Credentials:
    print(tokens)
    creds = None
    if tokens.get(user) != None:
        creds = Credentials.from_authorized_user_info(tokens.get(user), SCOPES)
        #creds = tokens.get(user)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            tokens[user] = json.loads(creds.to_json())
    writeFile()
    return creds

if __name__ == "__main__":
    authorize("TEST")

def writeFile():
    with open("tokens.json", "w") as f:
        f.write(json.dumps(tokens))

with open("tokens.json", "r") as f:
    content = f.read()
    cache = json.loads(content)
    for k, v in cache.items():
        tokens[k] = v
