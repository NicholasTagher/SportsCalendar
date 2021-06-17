from selenium import webdriver
import datetime


def get_teams(x="driver"):
    euro_teams = []
    euro_game_teams = x.find_elements_by_css_selector('span.abbrev')
    for team in euro_game_teams:
        euro_teams.append(team.text)

    return euro_teams


def get_times(x="driver"):
    euro_times = []
    euro_game_times = x.find_elements_by_css_selector('span.time.game-date.game-time')
    for time in euro_game_times:
        euro_times.append(time.text)
    euro_times = [x.replace(" ET", "") for x in euro_times]

    return euro_times


def get_networks(x="driver"):
    euro_networks = []
    euro_game_networks = x.find_elements_by_css_selector('span.network')
    for network in euro_game_networks:
        euro_networks.append(network.text)

    return euro_networks


def get_schedule(date):
    euro_start = datetime.date(2021, 6, 11)
    euro_end = datetime.date(2021, 7, 11)
    if euro_start <= date <= euro_end:
        chrome_driver_path = "..\ChromeDriver\chromedriver.exe"
        driver = webdriver.Chrome(executable_path=chrome_driver_path)
        driver.get('https://www.espn.com/soccer/scoreboard/_/league/UEFA.EURO/date/' + date.strftime('%Y%m%d'))
        teams = get_teams(driver)
        times = get_times(driver)
        networks = get_networks(driver)
        euro_games = []
        for i in range(0, len(networks)):
            euro_games.append(f"{teams[2 * i]} @ {teams[2 * i + 1]}, {times[i]}, {networks[i]}")
        driver.close()
    else:
        euro_games = None

    return euro_games