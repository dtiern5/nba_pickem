from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from teams_dict import convert_team_name
from find_stat import find_stat


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


def retrieve_answers(cards, player_list):
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
    stat_output = ''  # initialize
    if stat == 'rebounds':  # WORKING ON THIS ONE
        team_1_stat = float(df_team_per_game.loc[f'{team_1}'][16])
        team_1_opp_stat = float(df_opp_per_game.loc[f'{team_1}'][16])
        team_2_stat = float(df_team_per_game.loc[f'{team_2}'][16])
        team_2_opp_stat = float(df_opp_per_game.loc[f'{team_2}'][16])
        league_avg_stat = float(df_team_per_game.loc[f'League Average'][16])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        stat_output += f'{team_1}\n' if team_1_prediction > team_2_prediction else f'{team_2}\n'
        stat_output += f'   {team_1}: {team_1_stat} rebounds per game\n   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        stat_output += f'   {team_2}: {team_2_stat} rebounds per game\n   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'assists':
        team_1_stat = float(df_team_per_game.loc[f'{team_1}'][17])
        team_1_opp_stat = float(df_opp_per_game.loc[f'{team_1}'][17])
        team_2_stat = float(df_team_per_game.loc[f'{team_2}'][17])
        team_2_opp_stat = float(df_opp_per_game.loc[f'{team_2}'][17])
        league_avg_stat = float(df_team_per_game.loc[f'League Average'][17])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        stat_output += f'{team_1}\n' if team_1_prediction > team_2_prediction else f'{team_2}\n'
        stat_output += f'   {team_1}: {team_1_stat} assists per game\n   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        stat_output += f'   {team_2}: {team_2_stat} assists per game\n   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'steals':
        team_1_stat = float(df_team_per_game.loc[f'{team_1}'][18])
        team_1_opp_stat = float(df_opp_per_game.loc[f'{team_1}'][18])
        team_2_stat = float(df_team_per_game.loc[f'{team_2}'][18])
        team_2_opp_stat = float(df_opp_per_game.loc[f'{team_2}'][18])
        league_avg_stat = float(df_team_per_game.loc[f'League Average'][18])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        stat_output += f'{team_1}\n' if team_1_prediction > team_2_prediction else f'{team_2}\n'
        stat_output += f'   {team_1}: {team_1_stat} steals per game\n   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        stat_output += f'   {team_2}: {team_2_stat} steals per game\n   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'block':
        team_1_stat = float(df_team_per_game.loc[f'{team_1}'][19])
        team_1_opp_stat = float(df_opp_per_game.loc[f'{team_1}'][19])
        team_2_stat = float(df_team_per_game.loc[f'{team_2}'][19])
        team_2_opp_stat = float(df_opp_per_game.loc[f'{team_2}'][19])
        league_avg_stat = float(df_team_per_game.loc[f'League Average'][19])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        stat_output += f'{team_1}\n' if team_1_prediction > team_2_prediction else f'{team_2}\n'
        stat_output += f'   {team_1}: {team_1_stat} blocks per game\n   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        stat_output += f'   {team_2}: {team_2_stat} blocks per game\n   {team_2}: {team_2_prediction} weighted against {team_1}\n'


    elif stat == 'field goal':
        team_1_stat = float(df_team_per_game.loc[f'{team_1}'][4])
        team_1_opp_stat = float(df_opp_per_game.loc[f'{team_1}'][4])
        team_2_stat = float(df_team_per_game.loc[f'{team_2}'][4])
        team_2_opp_stat = float(df_opp_per_game.loc[f'{team_2}'][4])
        league_avg_stat = float(df_team_per_game.loc[f'League Average'][4])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 3)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 3)

        stat_output += f'{team_1}\n' if team_1_prediction > team_2_prediction else f'{team_2}\n'
        stat_output += f'   {team_1}: {team_1_stat} FG% per game\n   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        stat_output += f'   {team_2}: {team_2_stat} FG% per game\n   {team_2}: {team_2_prediction} weighted against {team_1}\n'


    elif stat == '3 pointers':
        team_1_stat = float(df_team_per_game.loc[f'{team_1}'][5])
        team_1_opp_stat = float(df_opp_per_game.loc[f'{team_1}'][5])
        team_2_stat = float(df_team_per_game.loc[f'{team_2}'][5])
        team_2_opp_stat = float(df_opp_per_game.loc[f'{team_2}'][5])
        league_avg_stat = float(df_team_per_game.loc[f'League Average'][5])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        stat_output += f'{team_1}\n' if team_1_prediction > team_2_prediction else f'{team_2}\n'
        stat_output += f'   {team_1}: {team_1_stat} 3 pointers per game\n   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        stat_output += f'   {team_2}: {team_2_stat} 3 pointers per game\n   {team_2}: {team_2_prediction} weighted against {team_1}\n'



    elif stat == 'free throws':
        team_1_stat = float(df_team_per_game.loc[f'{team_1}'][11])
        team_1_opp_stat = float(df_opp_per_game.loc[f'{team_1}'][11])
        team_2_stat = float(df_team_per_game.loc[f'{team_2}'][11])
        team_2_opp_stat = float(df_opp_per_game.loc[f'{team_2}'][11])
        league_avg_stat = float(df_team_per_game.loc[f'League Average'][11])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        stat_output += f'{team_1}\n' if team_1_prediction > team_2_prediction else f'{team_2}\n'
        stat_output += f'   {team_1}: {team_1_stat} free throws per game\n   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        stat_output += f'   {team_2}: {team_2_stat} free throws per game\n   {team_2}: {team_2_prediction} weighted against {team_1}\n'


    elif stat == 'first points':
        team_1_stat = float(df_team_per_game.loc[f'{team_1}'][22])
        team_1_opp_stat = float(df_opp_per_game.loc[f'{team_1}'][22])
        team_2_stat = float(df_team_per_game.loc[f'{team_2}'][22])
        team_2_opp_stat = float(df_opp_per_game.loc[f'{team_2}'][22])
        league_avg_stat = float(df_team_per_game.loc[f'League Average'][22])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        stat_output += f'{team_1}\n' if team_1_prediction > team_2_prediction else f'{team_2}\n'
        stat_output += f'   {team_1}: {team_1_stat} points per game\n   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        stat_output += f'   {team_2}: {team_2_stat} points per game\n   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'win':
        stat_output += f'{team_1}\n' if vegas.get(team_1) < vegas.get(team_2) else f'{team_2}\n'
        stat_output += f'   {team_1}: {str(vegas.get(team_1))}\n'
        stat_output += f'   {team_2}: {str(vegas.get(team_2))}\n'
    else:
        stat_output = 'Error in get_team_stat'

    return stat_output


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

    for i in range(len(player_stats)):
        if len(player_stats[i]) > 1:
            player_list.append(player_stats[i][0])
    return player_list


def compare_player_stats(player, stat):
    if stat == '3-pointers':
        pass
    if stat == 'assists':
        pass
    if stat == 'rebounds':
        pass
def main():
    driver = webdriver.Firefox()
    driver.implicitly_wait(2)
    soup = open_pickem_browser(driver)
    cards = create_question_cards(soup)
    print(cards)
    player_list = get_player_list(driver)
    vegas = get_vegas_lines(driver)
    soup = open_bball_ref_browser(driver)
    df_team_per_game = create_team_stats_df(soup)
    df_opp_per_game = create_opp_stats_df(soup)
    retrieve_answers(cards, player_list)


    # The final card format is [[team_1, team_2], question_text, relevant_stat, [player_1, player_2]]
    # cards[i][3] only exists for player questions
    for i, card in enumerate(cards):
        if 'team' in card[1]:
            print(f'Question {i + 1}: {card[1]}')
            print(compare_teams_stat(card[0][0], card[0][1], card[2], df_team_per_game, df_opp_per_game,
                                     vegas))
        else:
            print(f'Question {i + 1}: {card[1]}')
            for player in player_list:
                if player in card[1]:
                    print(compare_player_stats(player, card[2]))


    driver.quit()


if __name__ == "__main__":
    main()
