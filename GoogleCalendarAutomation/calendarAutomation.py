from __future__ import print_function
import csv
import datetime
import pickle
import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd

SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    print('Getting the calendar id of Appointments')
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])

    if not calendars:
        print('No calendars found.')
    for calendar in calendars:
        summary = calendar['summary']
        if(summary=='Appointments'):
            apptCalendarId = calendar['id']
            print(apptCalendarId)
    
    if not apptCalendarId:
        print('No access to the Appointment Calendar')

    # Call the `Calendar API
    csvFile = open(sys.argv[1],'r')

    readerFile = list(csv.reader(csvFile,delimiter=','))
    sortedlist = sorted(readerFile[1:], key=lambda row: row[0], reverse=False)
    dateSubClass = datetime.datetime

    for row in sortedlist:
        print('Creating an event')
        startDateTime = dateSubClass.strptime(row[1], "%d-%m-%Y %H:%M").isoformat()
        endDateTime = (dateSubClass.strptime(row[1], "%d-%m-%Y %H:%M") + datetime.timedelta(minutes=30)).isoformat()
        event = { 
                'summary': 'MD Install',
                'description': row[1] + ' ' + row[2],
                'creator': {'displayName':'Doug', 'email':'technicalanalytical2021@gmail.com'},
                'sendUpdates': True,
                'guestsCanSeeOtherGuests': True,
                'start' : {'dateTime': startDateTime, 'timeZone': 'America/New_York'}, 
                'end' :   {'dateTime': endDateTime, 'timeZone': 'America/New_York'},
                'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 15}]}
                }

        events_result = service.events().insert(calendarId=apptCalendarId, sendNotifications = True, body= event).execute()
    
        print(''' %s Event added ''' %events_result['description'])

if __name__ == '__main__':
    main()
