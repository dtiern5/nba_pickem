from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from teams_dict import convert_team_name
from teams_dict import convert_to_abbrev
from find_stat import find_stat
import unidecode
import unicodedata


def open_pickem_browser(driver):
    timeout = 25
    url = r"https://picks.nba.com/primetime-picks"
    driver.get(url)

    # Click out of of modal popup
    element_present = ec.presence_of_element_located(
        (By.XPATH, r"/html/body/div[1]/div[2]/div/div/button"))
    WebDriverWait(driver, timeout).until(element_present)
    element = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/button')
    element.click()

    # Create soup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def open_bball_ref_browser(driver):
    url = "https://www.basketball-reference.com/leagues/NBA_2021.html"
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_player_list(driver):
    player_list = []
    url = 'https://www.basketball-reference.com/leagues/NBA_2021_per_game.html'
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', attrs={'id': 'per_game_stats'})

    cols = table.thead.find_all('th')
    cols = [h.text.strip() for h in cols]
    cols = cols[1:]

    rows = table.find_all('tr')
    rows = rows[1:]
    player_stats = [[td.getText().strip() for td in rows[i].find_all('td')] for i in range(len(rows))]

    for i, player in enumerate(player_stats):
        if len(player_stats[i]) > 1:
            player_stats[i][0] = unidecode.unidecode(player_stats[i][0])

    for i in range(len(player_stats)):
        if len(player_stats[i]) > 1:
            player_list.append(player_stats[i][0])
    return player_list


def get_vegas_lines(driver):
    url = "https://sports.yahoo.com/nba/odds/"
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    div = soup.find('div', id='op-content-wrapper')

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

    driver.quit()


def create_question_cards(soup):
    # Each "card" contains two teams, and a question pertaining to them
    find_cards = soup.find_all('div', attrs={'class': 'PrimetimePicksMatchupstyled__PtpCardContainer-tdtza-0 fLNWPg'})

    # Create a list, each index is list of 2 teams and the question
    teams_and_q_list = []
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
        teams_and_q_list.append(temp)
    return teams_and_q_list


def create_team_stats_df(soup):
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

    df_team_per_game = pd.DataFrame(team_stats, columns=cols)
    df_team_per_game.set_index('Team', inplace=True)
    return df_team_per_game


def create_opp_stats_df(soup):
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

    df_opp_per_game = pd.DataFrame(opp_stats, columns=opp_cols)
    df_opp_per_game.set_index('Team', inplace=True)
    return df_opp_per_game


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
            player_stats[i][0] = unidecode.unidecode(player_stats[i][0])
    players_df = pd.DataFrame(player_stats, columns=cols)
    players_df.set_index('Player', inplace=True)
    return players_df


def create_usable_list(cards, player_list):
    for i, card in enumerate(cards):
        stat = find_stat(card[1])  # Find the stat in the question text('rebound', 'assists')
        cards[i].append(stat)
        players_in_question = []
        if 'team' not in card[1]:
            for player in player_list:
                if player in card[1] and player not in players_in_question:
                    players_in_question.append(player)
            cards[i].append(players_in_question)
    return cards


def compare_teams_stat(team_1, team_2, stat, df_team_per_game, df_opp_per_game, vegas):
    team_question_output = ''  # initialize
    if stat == 'rebounds':  # WORKING ON THIS ONE
        team_1_stat = float(df_team_per_game.loc[f'{team_1}'][16])
        team_1_opp_stat = float(df_opp_per_game.loc[f'{team_1}'][16])
        team_2_stat = float(df_team_per_game.loc[f'{team_2}'][16])
        team_2_opp_stat = float(df_opp_per_game.loc[f'{team_2}'][16])
        league_avg_stat = float(df_team_per_game.loc[f'League Average'][16])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        # team_question_output += f'{team_1}\n\n' if team_1_prediction > team_2_prediction else f'{team_2}\n\n'
        team_question_output += f'   {team_1}: {team_1_stat} rebounds per game\n   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        team_question_output += f'   {team_2}: {team_2_stat} rebounds per game\n   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'assists':
        team_1_stat = float(df_team_per_game.loc[f'{team_1}'][17])
        team_1_opp_stat = float(df_opp_per_game.loc[f'{team_1}'][17])
        team_2_stat = float(df_team_per_game.loc[f'{team_2}'][17])
        team_2_opp_stat = float(df_opp_per_game.loc[f'{team_2}'][17])
        league_avg_stat = float(df_team_per_game.loc[f'League Average'][17])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        # team_question_output += f'{team_1}\n\n' if team_1_prediction > team_2_prediction else f'{team_2}\n\n'
        team_question_output += f'   {team_1}: {team_1_stat} assists per game\n   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        team_question_output += f'   {team_2}: {team_2_stat} assists per game\n   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'steals':
        team_1_stat = float(df_team_per_game.loc[f'{team_1}'][18])
        team_1_opp_stat = float(df_opp_per_game.loc[f'{team_1}'][18])
        team_2_stat = float(df_team_per_game.loc[f'{team_2}'][18])
        team_2_opp_stat = float(df_opp_per_game.loc[f'{team_2}'][18])
        league_avg_stat = float(df_team_per_game.loc[f'League Average'][18])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        # team_question_output += f'{team_1}\n\n' if team_1_prediction > team_2_prediction else f'{team_2}\n\n'
        team_question_output += f'   {team_1}: {team_1_stat} steals per game\n   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        team_question_output += f'   {team_2}: {team_2_stat} steals per game\n   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'block':
        team_1_stat = float(df_team_per_game.loc[f'{team_1}'][19])
        team_1_opp_stat = float(df_opp_per_game.loc[f'{team_1}'][19])
        team_2_stat = float(df_team_per_game.loc[f'{team_2}'][19])
        team_2_opp_stat = float(df_opp_per_game.loc[f'{team_2}'][19])
        league_avg_stat = float(df_team_per_game.loc[f'League Average'][19])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        # team_question_output += f'{team_1}\n\n' if team_1_prediction > team_2_prediction else f'{team_2}\n\n'
        team_question_output += f'   {team_1}: {team_1_stat} blocks per game\n   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        team_question_output += f'   {team_2}: {team_2_stat} blocks per game\n   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'field goal':
        team_1_stat = float(df_team_per_game.loc[f'{team_1}'][4])
        team_1_opp_stat = float(df_opp_per_game.loc[f'{team_1}'][4])
        team_2_stat = float(df_team_per_game.loc[f'{team_2}'][4])
        team_2_opp_stat = float(df_opp_per_game.loc[f'{team_2}'][4])
        league_avg_stat = float(df_team_per_game.loc[f'League Average'][4])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 3)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 3)

        # team_question_output += f'{team_1}\n\n' if team_1_prediction > team_2_prediction else f'{team_2}\n\n'
        team_question_output += f'   {team_1}: {team_1_stat} FG% per game\n   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        team_question_output += f'   {team_2}: {team_2_stat} FG% per game\n   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'threes':
        team_1_stat = float(df_team_per_game.loc[f'{team_1}'][5])
        team_1_opp_stat = float(df_opp_per_game.loc[f'{team_1}'][5])
        team_2_stat = float(df_team_per_game.loc[f'{team_2}'][5])
        team_2_opp_stat = float(df_opp_per_game.loc[f'{team_2}'][5])
        league_avg_stat = float(df_team_per_game.loc[f'League Average'][5])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        # team_question_output += f'{team_1}\n\n' if team_1_prediction > team_2_prediction else f'{team_2}\n\n'
        team_question_output += f'   {team_1}: {team_1_stat} 3 pointers per game\n   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        team_question_output += f'   {team_2}: {team_2_stat} 3 pointers per game\n   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'free throws':
        team_1_stat = float(df_team_per_game.loc[f'{team_1}'][11])
        team_1_opp_stat = float(df_opp_per_game.loc[f'{team_1}'][11])
        team_2_stat = float(df_team_per_game.loc[f'{team_2}'][11])
        team_2_opp_stat = float(df_opp_per_game.loc[f'{team_2}'][11])
        league_avg_stat = float(df_team_per_game.loc[f'League Average'][11])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        # team_question_output += f'{team_1}\n\n' if team_1_prediction > team_2_prediction else f'{team_2}\n\n'
        team_question_output += f'   {team_1}: {team_1_stat} free throws per game\n   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        team_question_output += f'   {team_2}: {team_2_stat} free throws per game\n   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'points':
        team_1_stat = float(df_team_per_game.loc[f'{team_1}'][22])
        team_1_opp_stat = float(df_opp_per_game.loc[f'{team_1}'][22])
        team_2_stat = float(df_team_per_game.loc[f'{team_2}'][22])
        team_2_opp_stat = float(df_opp_per_game.loc[f'{team_2}'][22])
        league_avg_stat = float(df_team_per_game.loc[f'League Average'][22])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        # team_question_output += f'{team_1}\n' if team_1_prediction > team_2_prediction else f'{team_2}\n\n'
        team_question_output += f'   {team_1}: {team_1_stat} points per game\n   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        team_question_output += f'   {team_2}: {team_2_stat} points per game\n   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'win':
        team_question_output += f'{team_1}\n\n' if vegas.get(team_1) < vegas.get(team_2) else f'{team_2}\n\n'
        team_question_output += f'   {team_1}: {str(vegas.get(team_1))}\n'
        team_question_output += f'   {team_2}: {str(vegas.get(team_2))}\n'
    else:
        team_question_output = 'Error in get_team_stat'

    return team_question_output


# TODO: This is temporary, should merge with manual input if possible
def compare_player_stats(players, stat, df_players, df_opp_per_game, teams):
    player_question_output = ''
    team_abbrs = []

    for team in teams:
        team_abbrs.append(convert_to_abbrev[team])

    for player in players:
        for team in team_abbrs: # TODO: Make this work for traded players, probably another for loop through df_players
            if df_players.loc[player][2] != team:
                opp_team_abbr = team
        for team, abbr in convert_to_abbrev.items():
            if abbr == opp_team_abbr:
                opp_team = team
        if stat.lower() == 'threes':
            player_threes = float(df_players.loc[player][9])
            defense_threes = float(df_opp_per_game.loc[f'{opp_team}'][7])
            league_threes_avg = float(df_opp_per_game.loc['League Average'][7])
            predicted_threes = round(player_threes * (defense_threes / league_threes_avg), 1)

            player_question_output += (f'   {player}: {player_threes} 3s per game\n')
            player_question_output += (
                f'   Against {opp_team}\'s defense, {player} will hit {predicted_threes} threes\n')

        elif stat == 'assists':
            player_assists = float(df_players.loc[player][22])
            def_assists = float(df_opp_per_game.loc[f'{opp_team}'][17])
            league_assists_avg = float(df_opp_per_game.loc['League Average'][17])
            predicted_assists = round(player_assists * (def_assists / league_assists_avg), 1)

            player_question_output += (f'   {player}: {player_assists} assists per game\n')
            player_question_output += (
                f'   Against {opp_team}\'s defense, {player} will dish {predicted_assists} assists\n')

        elif stat == 'rebounds':
            player_rebounds = float(df_players.loc[player][21])
            def_rebounds = float(df_opp_per_game.loc[f'{opp_team}'][16])
            league_rebounds_avg = float(df_opp_per_game.loc['League Average'][16])
            predicted_rebounds = round(player_rebounds * (def_rebounds / league_rebounds_avg), 1)

            player_question_output += (f'   {player}: {player_rebounds} rebounds per game\n')
            player_question_output += (
                f'   Against {opp_team}\'s defense, {player} will grab {predicted_rebounds} rebounds\n')

        elif stat == 'points':
            points_from_two = float(df_players.loc[player][12]) * 2
            points_from_three = float(df_players.loc[player][9]) * 3
            points_from_ft = float(df_players.loc[player][16])

            defense_twos = float(df_opp_per_game.loc[f'{opp_team}'][10])
            defense_threes = float(df_opp_per_game.loc[f'{opp_team}'][7])

            league_twos_avg = float(df_opp_per_game.loc['League Average'][10])
            league_threes_avg = float(df_opp_per_game.loc['League Average'][7])

            predicted_points = round(points_from_two * (defense_twos / league_twos_avg) + points_from_three * (
                        defense_threes / league_threes_avg) + points_from_ft, 1)

            player_question_output += (f'   {player}: {df_players.loc[player][27]}ppg\n')
            player_question_output += (f'   Against {opp_team}: {player} will score {predicted_points} points\n')

    return player_question_output


def manual_entry(df_players, df_opp_per_game):
    stat_list = ['assists', 'points', 'rebounds', 'threes']

    player = input("Player's full name: ")
    if player not in df_players.index:
        print('Use full player name\n')
        manual_entry(df_players, df_opp_per_game)

    stat = input("Stat in question: ")
    if stat.lower() not in stat_list:
        print("Viable stats are 'assists', 'points', 'rebounds', 'threes'\n")
        manual_entry(df_players, df_opp_per_game)

    opposing_input = input("Opposing team: ")
    if opposing_input not in df_opp_per_game.index:
        print("Needs full location and team name (Ex: 'Minnesota Timberwolves')\n")
        manual_entry(df_players, df_opp_per_game)

    player_question_output = ''
    if stat.lower() == 'threes':
        player_threes = float(df_players.loc[player][9])
        defense_threes = float(df_opp_per_game.loc[f'{opposing_input}'][7])
        league_threes_avg = float(df_opp_per_game.loc['League Average'][7])
        predicted_threes = round(player_threes * (defense_threes / league_threes_avg), 1)

        player_question_output += (f'   {player}: {player_threes} 3s per game\n')
        player_question_output += (f'   Against {opposing_input}\'s defense, {player} will hit {predicted_threes} threes\n')

    elif stat.lower() == 'assists':
        player_assists = float(df_players.loc[player][22])
        def_assists = float(df_opp_per_game.loc[f'{opposing_input}'][17])
        league_assists_avg = float(df_opp_per_game.loc['League Average'][17])
        predicted_assists = round(player_assists * (def_assists / league_assists_avg), 1)

        player_question_output += (f'   {player}: {player_assists} assists per game\n')
        player_question_output += (f'   Against {opposing_input}\'s defense, {player} will dish {predicted_assists} assists\n')

    elif stat.lower() == 'rebounds':
        player_rebounds = float(df_players.loc[player][21])
        def_rebounds = float(df_opp_per_game.loc[f'{opposing_input}'][16])
        league_rebounds_avg = float(df_opp_per_game.loc['League Average'][16])
        predicted_rebounds = round(player_rebounds * (def_rebounds / league_rebounds_avg), 1)

        player_question_output += (f'   {player}: {player_rebounds} rebounds per game\n')
        player_question_output += (f'   Against {opposing_input}\'s defense, {player} will grab {predicted_rebounds} rebounds\n')


    elif stat.lower() == 'points':
        points_from_two = float(df_players.loc[player][12]) * 2
        points_from_three = float(df_players.loc[player][9]) * 3
        points_from_ft = float(df_players.loc[player][16])

        defense_twos = float(df_opp_per_game.loc[f'{opposing_input}'][10])
        defense_threes = float(df_opp_per_game.loc[f'{opposing_input}'][7])

        league_twos_avg = float(df_opp_per_game.loc['League Average'][10])
        league_threes_avg = float(df_opp_per_game.loc['League Average'][7])

        predicted_points = round(points_from_two * (defense_twos/league_twos_avg) + points_from_three * (defense_threes/league_threes_avg) + points_from_ft, 1)

        player_question_output += (f'   {player}: {df_players.loc[player][27]}ppg\n')
        player_question_output += (f'   Against {opposing_input}: {player} will score {predicted_points} points\n')

    else:
        player_question_output += 'Error in players stats'
    print(player_question_output)

    run_prompt = input('Another player? Y/N\n')
    if run_prompt.lower() == 'y':
        manual_entry(df_players, df_opp_per_game)
    else:
        print('Goodbye')
        return


def user_method_prompt(df_players, df_team_per_game, df_opp_per_game, player_list, vegas):
    user_method = input('Manual or Auto?\n')
    if user_method.lower() == 'manual':
        manual_entry(df_players, df_opp_per_game)
    elif user_method.lower() == 'auto':
        cards = [[['Boston Celtics', 'Miami Heat'], 'Which team will dish more assists?'],
                 [['Atlanta Hawks', 'Minnesota Timberwolves'], 'Which team will grab more rebounds?'],
                 [['Los Angeles Clippers', 'Washington Wizards'], 'Which team have more steals?'],
                 [['Atlanta Hawks', 'Minnesota Timberwolves'], 'Will Anthony Edwards score more than 0 points?'],
                 [['Minnesota Timberwolves', 'Golden State Warriors'], 'Who will hit more 3 pointers? Anthony Edwards or Stephen Curry'],
                 [['Atlanta Hawks', 'Minnesota Timberwolves'], 'Will Ricky Rubio score more than 8 points?'],
                 [['Milwaukee Bucks', 'Miami Heat'], 'Who will score more points? Giannis Antetokounmpo or Jimmy Butler'],
                 [['Utah Jazz', 'Philadelphia 76ers'], 'Who will grab more rebounds? Joel Embiid or Rudy Gobert'],
                 [['Phoenix Suns', 'Atlanta Hawks'], 'Who will dish more assists? Chris Paul or Trae Young'],
                 [['Toronto Raptors', 'Denver Nuggets'], 'Who will score more points? Fred VanVleet or Nikola Jokic']]



        create_usable_list(cards, player_list)

        # The final card format is [[team_1, team_2], question_text, relevant_stat, [player_1, player_2]]
        # cards[i][3] only exists for player questions
        for i, card in enumerate(cards):
            if 'team' in card[1]:
                print(f'Question {i + 1}: {card[1]}, {card[0][0]} or {card[0][1]}')
                print(compare_teams_stat(card[0][0], card[0][1], card[2], df_team_per_game, df_opp_per_game,
                                         vegas))
            else:
                print(f'Question {i + 1}: {card[1]}')
                print(compare_player_stats(card[3], card[2], df_players, df_opp_per_game, card[0]))
    elif user_method.lower() == 'q':
        print('Exiting...')
        return
    else:
        print("Viable inputs are 'Manual', 'Auto', or 'q' for quit")

def main():
    print("Please wait, scraping data from web and organizing into dataframes")
    print("This can take a minute")
    driver = webdriver.Firefox()
    driver.implicitly_wait(1)
    # soup = open_pickem_browser(driver)
    # cards = create_question_cards(soup)
    player_list = get_player_list(driver)
    vegas = get_vegas_lines(driver)
    soup = open_bball_ref_browser(driver)
    df_team_per_game = create_team_stats_df(soup)
    df_opp_per_game = create_opp_stats_df(soup)
    df_players = create_players_df(driver)
    driver.quit()

    user_method_prompt(df_players, df_team_per_game, df_opp_per_game, player_list, vegas)


if __name__ == "__main__":
    main()
