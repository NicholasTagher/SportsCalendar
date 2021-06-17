from selenium import webdriver

team_dictionary = {
    '76ers': 'PHI',
    'Nets': 'BKN',
    'Bucks': 'MIL',
    'Hawks': 'ATL',
    'Jazz': 'UTA',
    'Suns': 'PHX',
    'Clippers': 'LAC',
}


def get_teams(x="driver"):
    nba_teams = []
    nba_game_teams = x.find_elements_by_css_selector('span.sb-team-short')
    for team in nba_game_teams:
        nba_teams.append(team_dictionary[team.text])

    return nba_teams


def get_times(x="driver"):
    nba_times = []
    nba_game_times = x.find_elements_by_css_selector('th span.time')
    for time in nba_game_times:
        nba_times.append(time.text)
    nba_times = [x.replace(" ET", "") for x in nba_times]

    return nba_times


def get_networks(x="driver"):
    nba_networks = []
    nba_game_networks = x.find_elements_by_css_selector('th.network')
    for network in nba_game_networks:
        nba_networks.append(network.text)

    return nba_networks


# def get_schedule(nba_teams, nba_times, nba_networks):
#     nba_schedule = []
#     for i in range(0, len(nba_networks)):
#         nba_schedule.append(f"{nba_teams[2 * i]} @ {nba_teams[2 * i + 1]}, {nba_times[i]}, {nba_networks[i]}")
#
#     return nba_schedule


def get_schedule(date):
    chrome_driver_path = "..\ChromeDriver\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get('https://www.espn.com/nba/scoreboard/_/date/' + date.strftime('%Y%m%d'))
    teams = get_teams(driver)
    times = get_times(driver)
    networks = get_networks(driver)
    nba_games = []
    for i in range(0, len(networks)):
        nba_games.append(f"{teams[2 * i]} @ {teams[2 * i + 1]}, {times[i]}, {networks[i]}")

    return nba_games
