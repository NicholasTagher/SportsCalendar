from bs4 import BeautifulSoup
from selenium import webdriver
import requests


team_dictionary = {
    'Islanders': 'NYI',
    'Lightning': 'TBL',
    'Golden Knights': 'VGK',
    'Canadiens': 'MTL',
}


def get_site(date):
    response = requests.get("https://www.espn.com/nhl/scoreboard/_/date/" + date.strftime('%Y%m%d'))
    espn_nhl_page = response.text
    soup = BeautifulSoup(espn_nhl_page, "html.parser")

    return soup


def get_teams(x):
    nhl_teams = []
    nhl_game_teams = x.find_all(name='div',
                                class_="ScoreCell__TeamName ScoreCell__TeamName--shortDisplayName truncate db")
    for team in nhl_game_teams:
        nhl_teams.append(team_dictionary[team.text])

    return nhl_teams


def get_times(date):
    chrome_driver_path = "..\ChromeDriver\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get('https://www.espn.com/nhl/scoreboard/_/date/' + date.strftime('%Y%m%d'))

    nhl_times = []
    nhl_game_times = driver.find_elements_by_css_selector(
        'div.ScoreCell__Time.ScoreboardScoreCell__Time.h9.clr-gray-03')
    for time in nhl_game_times:
        nhl_times.append(time.text.upper())
    driver.close()

    return nhl_times


def get_networks(x):
    nhl_networks = []
    nhl_game_networks = x.find_all(name='div', class_="ScoreCell__NetworkItem")
    for network in nhl_game_networks:
        nhl_networks.append(network.text)
    nhl_networks = [y.replace("NBCSN", "NBCS") for y in nhl_networks]

    return nhl_networks


def get_schedule(date):
    soup = get_site(date)
    teams = get_teams(soup)
    times = get_times(date)
    networks = get_networks(soup)
    nhl_games = []
    for i in range(0, len(networks)):
        nhl_games.append(f"{teams[2 * i]} @ {teams[2 * i + 1]}, {times[i]}, {networks[i]}")

    return nhl_games
