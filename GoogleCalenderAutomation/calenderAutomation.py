from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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
            flow = InstalledAppFlow.from_client_secrets_file(
                'C:/Users/chait/Documents/creds/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Creating an event') 
    event1 = { 
            'summary': 'House of Cards',
            'creator': {'displayName':'Frank Underwood', 'self' : True, 'email':'technicalanalytical2021@gmail.com'},
            'attendees': [{'displayName':'Chay', 'email':'cpboddeti@gmail.com'},{'displayName':'Doug Stamper','email':'chaitanyaprasad1111@gm'}],
            'visibility': 'private',
            'locked': True,
            'guestsCanSeeOtherGuests': False,
            'start' : {'dateTime': '2021-01-28T11:00:00','timeZone': 'America/New_York'}, 
            'end' :   {'dateTime': '2021-01-29T13:00:00','timeZone': 'America/New_York'}
            }
    
    events_result = service.events().insert(calendarId='primary', sendNotifications = True, body= event1).execute()
    
    print(''' %r event added:
        Start: %s
        End: %s''' %(events_result['summary'].encode('utf-8'),events_result['start']['dateTime'],events_result['end']['dateTime']))

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])


if __name__ == '__main__':
    main()