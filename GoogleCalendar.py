import datetime as dt
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
secrets_file = 'credentials.json'
class GoogleCalendar:

    def __init__(self, credentials):
        self.creds = credentials

    def get_credentials(self, secrets_file):
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(secrets_file, SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            #with open('token.pickle', 'wb') as token:
            #    pickle.dump(creds, token)
            return self.creds



    def fetchEvents(self, cal_id, time_min, time_max):
            service = build('calendar', 'v3', credentials=self.creds)

            page_token = None
            result = []
            max_date = dt.datetime.strptime(time_max[:-6], '%Y-%m-%dT%H:%M:%S')
            while True:
                events_result = service.events().list(calendarId=cal_id, timeMin=time_min,
                                                      timeMax=time_max, singleEvents=True, pageToken=page_token).execute()
                events = events_result.get('items', [])

                if not events:
                    print('No upcoming events found.')

                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    end = event['end'].get('dateTime', event['end'].get('date'))
                    if len(start) > 10:
                        stdt = dt.datetime.strptime(start[:-6], '%Y-%m-%dT%H:%M:%S')
                        endt = dt.datetime.strptime(end[:-6], '%Y-%m-%dT%H:%M:%S')
                    else:
                        stdt = dt.datetime.strptime(start, '%Y-%m-%d')
                        endt = dt.datetime.strptime(end, '%Y-%m-%d')

                    delta = (endt - stdt)
                    print("Delta :" ,delta.days)
                    for i in range(delta.days):
                        dayDate = stdt + dt.timedelta(days=i)
                        # No need to count days after the end of the specified period
                        print(dayDate, max_date)
                        if (dayDate <= max_date):
                            result.append((dayDate, event['summary']))
                            # print(str(dayDate), event['summary'])
                        else:
                            break

                page_token = events_result.get('nextPageToken')
                if not page_token:
                    return result

#def get_events():
#    YEAR="2020"
#    MONTH="04"
#    LAST_DAY="30"
#    events = GoogleCalendar.fetchEvents("raph.mic@gmail.com", f"{YEAR}-{MONTH}-01T00:00:00+01:00", f"{YEAR}-{MONTH}-{LAST_DAY}T23:59:59+01:00")
#    return events

#print(get_events())