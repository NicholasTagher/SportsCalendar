# Download the helper library from https://www.twilio.com/docs/python/install
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import datetime
from twilio.rest import Client

chrome_driver_path = "..\ChromeDriver\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'XXXXXXX'
auth_token = 'XXXXXXX'
client = Client(account_sid, auth_token)

team_dictionary = {
    # NHL
    'Flames': 'CGY',
    'Canucks': 'VAN',
    'Islanders': 'NYI',
    'Penguins': 'PIT',
    'Lightning': 'TB',
    'Panthers': 'FLA',
    'Wild': 'MIN',
    'Golden Knights': 'VGK',
    'Capitals': 'WSH',
    'Bruins': 'BOS',
    'Hurricanes': 'CAR',
    'Predators': 'NSH',
    'Blues': 'STL',
    'Avalanche': 'COL',
    'Maple Leafs': 'TOR',
    'Canadiens': 'MTL',
    'Jets': 'WPG',
    'Oilers': 'EDM',
    # NBA
    '76ers': 'PHI',
    'Nets': 'BKN',
    'Bucks': 'MIL',
    'Knicks': 'NYK',
    'Hawks': 'ATL',
    'Heat': 'MIA',
    'Celtics': 'BOS',
    'Wizards': 'WSH',
    'Pacers': 'IND',
    'Hornets': 'CHA',
    'Jazz': 'UTA',
    'Suns': 'PHX',
    'Nuggets': 'DEN',
    'Clippers': 'LAC',
    'Mavericks': 'DAL',
    'Blazers': 'POR',
    'Lakers': 'LAL',
    'Warriors': 'GSW',
    'Grizzlies': 'MEM',
    'Spurs': 'SA'
}

# NHL Section--------------------------------------------------------------------------------
today = datetime.date.today().strftime('%Y%m%d')
response = requests.get("https://www.espn.com/nhl/scoreboard/_/date/" + today)
espn_nhl_page = response.text
soup = BeautifulSoup(espn_nhl_page, "html.parser")

nhl_teams = []
nhl_game_teams = soup.find_all(name='div',
                               class_="ScoreCell__TeamName ScoreCell__TeamName--shortDisplayName truncate db")
for team in nhl_game_teams:
    nhl_teams.append(team.text)
nhl_teams = [team_dictionary[i] for i in nhl_teams]

nhl_times = []
driver.get('https://www.espn.com/nhl/scoreboard/_/date/' + today)
nhl_game_times = driver.find_elements_by_css_selector('div.ScoreCell__Time.ScoreboardScoreCell__Time.h9.clr-gray-03')
for time in nhl_game_times:
    nhl_times.append(time.text)
nhl_times = [x.upper() for x in nhl_times]
driver.close()

nhl_networks = []
nhl_game_networks = soup.find_all(name='div', class_="ScoreCell__NetworkItem")
for network in nhl_game_networks:
    nhl_networks.append(network.text)
nhl_networks = [x.replace("NBCSN","NBCS") for x in nhl_networks]

nhl_schedule = []
for i in range(0, len(nhl_networks)):
    nhl_schedule.append(f"{nhl_teams[2 * i]} @ {nhl_teams[2 * i + 1]}, {nhl_times[i]}, {nhl_networks[i]}")

text_message = f"Today's games:\n\nNHL:"
for game in nhl_schedule:
    text_message += f"\n {game}"
#print(text_message)
# End NHL Section--------------------------------------------------------------------------------

# NBA Section--------------------------------------------------------------------------------
chrome_driver_path = "..\ChromeDriver\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get('https://www.espn.com/nba/scoreboard/_/date/' + today)

nba_teams = []
nba_game_teams = driver.find_elements_by_css_selector('span.sb-team-short')
for team in nba_game_teams:
    nba_teams.append(team.text)
nba_teams = [team_dictionary[i] for i in nba_teams]

nba_times = []
nba_game_times = driver.find_elements_by_css_selector('th span.time')
for time in nba_game_times:
    nba_times.append(time.text)
nba_times = [x.replace(" ET", "") for x in nba_times]

nba_networks = []
nba_game_networks = driver.find_elements_by_css_selector('th.network')
for network in nba_game_networks:
    nba_networks.append(network.text)
driver.close()

nba_schedule = []
for i in range(0, len(nba_networks)):
    nba_schedule.append(f"{nba_teams[2 * i]} @ {nba_teams[2 * i + 1]}, {nba_times[i]}, {nba_networks[i]}")

text_message += "\n\nNBA:"
for game in nba_schedule:
    text_message += f"\n {game}"
print(text_message)
# End NBA Section--------------------------------------------------------------------------------

message = client.messages \
                .create(
                     body= f"\n{text_message}",
                     from_='+XXXXXXX',
                     to='+XXXXXXX'
                 )

print(message.sid)
