from __future__ import print_function
from turtle import st

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = FastAPI()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

@app.get("/items/")
async def read_item(summary: str, destination: str, description: str, depart_date: str, depart_time: str):

  event = {
  'summary': summary,
  'location': destination,
  'description': description,
  'start': {
    'dateTime': '{}T{}'.format(depart_date, depart_time),
    'timeZone': 'Asia/Tehran',
  },
  'end': {
    'dateTime': '{}T{}'.format(depart_date, depart_time),
    'timeZone': 'Asia/Tehran',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ],
  'attendees': [
    {'email': 'arghavan.souki.as@gmail.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

  creds = None
      # The file token.json stores the user's access and refresh tokens, and is
      # created automatically when the authorization flow completes for the first
      # time.
  if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
      # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)
          # Save the credentials for the next run
    with open('token.json', 'w') as token:
      token.write(creds.to_json())

  try:
    service = build('calendar', 'v3', credentials=creds)
    event = service.events().insert(calendarId='primary', body=event).execute()
    return RedirectResponse(event.get('htmlLink'))
          
  except HttpError as error:
    return(error)
