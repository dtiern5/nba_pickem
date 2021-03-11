from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from teams_dict import convert_team_name
import unidecode


# Scrape NBA Pickem information
def curr_pickem_qs(driver):
    timeout = 25
    url = r"https://picks.nba.com/primetime-picks"
    driver.get(url)

    # Click out of of modal popup
    element_present = ec.presence_of_element_located(
        (By.XPATH, r"/html/body/div[1]/div[2]/div/div/button"))
    WebDriverWait(driver, timeout).until(element_present)
    element = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/button')
    element.click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    find_cards = soup.find_all('div', attrs={'class': 'PrimetimePicksMatchupstyled__PtpCardContainer-tdtza-0 fLNWPg'})

    # Create a list, each index is list of 2 teams and the question
    curr_cards = []
    for index, card in enumerate(find_cards):
        current_matchup = []
        matchup = [logo.img['alt'] for logo in find_cards[index].find_all('div', attrs={
            'class': 'PrimetimePicksMatchupHeaderstyled__Team-sc-1w9xma9-3'})]
        for match in matchup:
            match = convert_team_name[match]
            current_matchup.append(match)
        question_text = find_cards[index].find('div', attrs={
            'class': 'PropCardstyled__QuestionText-sc-1nx4amu-3 ivUoYa'}).text.strip()
        temp = [current_matchup, question_text]
        curr_cards.append(temp)
    return curr_cards


# Simple list of players from Basketball Reference used for finding players in specific questions (cards_add_info)
def retrieve_player_list(driver):
    url = 'https://www.basketball-reference.com/leagues/NBA_2021_per_game.html'
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', attrs={'id': 'per_game_stats'})

    rows = table.find_all('tr')
    rows = rows[1:]
    player_stats = [[td.getText().strip() for td in rows[i].find_all('td')] for i in range(len(rows))]

    for i, player in enumerate(player_stats):
        if len(player_stats[i]) > 1:
            player_stats[i][0] = unidecode.unidecode(player_stats[i][0])  # Remove accents (e.g. Dončić to Doncic)

    player_list = []
    for i in range(len(player_stats)):
        if len(player_stats[i]) > 1:
            player_list.append(player_stats[i][0])
    return player_list


# Create dataframe of all NBA player stats
def create_players_df(driver):
    url = 'https://www.basketball-reference.com/leagues/NBA_2021_per_game.html'
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', attrs={'id': 'per_game_stats'})

    cols = table.thead.find_all('th')
    cols = [h.text.strip() for h in cols]
    cols = cols[1:]

    rows = table.find_all('tr')

    player_stats = [[td.getText().strip() for td in rows[i].find_all('td')] for i in range(len(rows))]
    player_stats = player_stats[1:]
    for i, player in enumerate(player_stats):
        if len(player_stats[i]) > 1:
            player_stats[i][0] = unidecode.unidecode(player_stats[i][0])  # Remove accents from names
        else:
            player_stats.remove(player_stats[i])  # Removes mid-table headers

    for i in range(len(player_stats)):
        if (i + 2) < len(player_stats):  # Changes traded players' team to their current, uses "total" for stats
            if player_stats[i][0] == player_stats[i + 2][0]:
                player_stats[i][3] = player_stats[i + 2][3]
                player_stats.remove(player_stats[i + 2])  # Removes specific instances of traded players
                player_stats.remove(player_stats[i + 1])
    players_df = pd.DataFrame(player_stats, columns=cols)
    players_df.set_index('Player', inplace=True)
    return players_df


# Get vegas odds if available
def retrieve_vegas_odds(driver):
    url = "https://sports.yahoo.com/nba/odds/"
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find_all('table', class_='W(100%) Maw(750px)')

    teams = [[t.getText() for t in tables[i].find_all('span', class_='Fw(600) Pend(4px)')] for i in range(len(tables))]
    teams = teams[:-1]  # Gets rid of "Featured Odds" game
    teams_list = []
    for match in teams:
        for team in match:
            teams_list.append(team)

    point_spreads = soup.find_all('div', class_='sixpack-bet-ODDS_POINT_SPREAD D(f) Fld(c) Ai(c)')
    odds = [[o.getText() for o in point_spreads[i].find_all('span', class_='Lh(19px)')[0::1]] for i in
            range(len(point_spreads))]

    odds_list = []
    for matchup in odds:
        for odd in matchup:
            odd = float(odd)
            if abs(odd) < 100:
                odds_list.append(odd)

    vegas_dict = dict(zip(teams_list, odds_list))
    return vegas_dict


# Create dataframe of all NBA team stats
def create_team_df(driver):
    url = "https://www.basketball-reference.com/leagues/NBA_2021.html"
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Find 'Team Per Game Stats' table
    table = soup.find('table', attrs={'id': 'team-stats-per_game'})

    # Create column headers
    cols = table.tr.find_all('th')
    cols = [h.text.strip() for h in cols]

    # Get data in rows
    rows = table.find_all('tr')
    team_stats = [[td.getText().strip() for td in rows[i].find_all('td')] for i in range(len(rows))]

    # Get rid of 'rank' column
    cols = cols[1:]
    team_stats = team_stats[1:]

    team_df = pd.DataFrame(team_stats, columns=cols)
    team_df.set_index('Team', inplace=True)
    return team_df


# Create dataframe of all NBa team stats 'against'
def create_opp_df(driver):
    url = "https://www.basketball-reference.com/leagues/NBA_2021.html"
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Find 'Opponent Per Game Stats' table
    opp_stats_table = soup.find('table', attrs={'id': 'opponent-stats-per_game'})

    # Create column headers
    opp_cols = opp_stats_table.tr.find_all('th')
    opp_cols = [h.text.strip() for h in opp_cols]

    # Get data in rows
    opp_rows = opp_stats_table.find_all('tr')
    opp_stats = [[td.getText().strip() for td in opp_rows[i].find_all('td')] for i in range(len(opp_rows))]

    # Get rid of rank column
    opp_cols = opp_cols[1:]
    opp_stats = opp_stats[1:]

    opp_df = pd.DataFrame(opp_stats, columns=opp_cols)
    opp_df.set_index('Team', inplace=True)
    return opp_df
