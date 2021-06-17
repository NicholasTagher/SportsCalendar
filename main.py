# This is the main file
import datetime
import calendar
import nhl
import nba
import euro
import os
from twilio.rest import Client

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
two_days = today + datetime.timedelta(days=2)
days = [tomorrow, two_days]

def compose_message(date):
    string = "\nNHL:"
    for game in nhl.get_schedule(date):
        string += f"\n {game}"
    string += "\n\nNBA:"
    for game in nba.get_schedule(date):
        string += f"\n {game}"
    string += "\n\nEuro:"
    for game in euro.get_schedule(date):
        string += f'\n {game}'

    return string

text_message = f"Today--{calendar.day_name[today.weekday()][0:3]} {today.strftime('%m/%d/%y')}"
text_message += compose_message(today)
text_message += f"\n\nTomorrow--{calendar.day_name[tomorrow.weekday()][0:3]} {tomorrow.strftime('%m/%d/%y')}"
text_message += compose_message(tomorrow)
# print(text_message)


account_sid = os.environ.get('TWILIO_ACCT_ID')
auth_token = os.environ.get('TWILIO_TOKEN')
client = Client(account_sid, auth_token)
twilio_number = os.environ.get('TWILIO_NUMBER')
phone_number = os.environ.get('MY_CELL')

message = client.messages \
                .create(
                     body = f"{text_message}",
                     from_= twilio_number,
                     to = phone_number
                 )
print(message.sid)
 