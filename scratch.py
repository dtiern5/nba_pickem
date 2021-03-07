from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from teams_dict import convert_to_abbrev


def create_players_df(driver):
    driver.implicitly_wait(1)
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

    players_df = pd.DataFrame(player_stats, columns=cols)
    players_df.set_index('Player', inplace=True)

    return players_df


def create_opp_stats_df(driver):
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

    df_opp_per_game = pd.DataFrame(opp_stats, columns=opp_cols)
    df_opp_per_game.set_index('Team', inplace=True)
    return df_opp_per_game


def compare_player_stats(players, stat, df_players, df_opp_per_game, teams):
    player_question_output = ''
    team_abbrs = []
    print('teams: ', teams)
    for team in teams:
        team_abbrs.append(convert_to_abbrev[team])
    print('team abbrs: ', team_abbrs)

    player_question_output = ''
    for player in players:
        for team in team_abbrs:
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

            player_question_output += (f'   {player} hits {player_threes} 3s per game\n')
            player_question_output += (
                f'   Against {opp_team}\'s defense, {player} will hit {predicted_threes} threes\n')
    return player_question_output

def main():
    driver = webdriver.Firefox()
    df_players = create_players_df(driver)
    df_opp_per_game = create_opp_stats_df(driver)

    card = [['Utah Jazz', 'Minnesota Timberwolves'], 'Who will hit more 3 pointers? Mike Conley or Anthony Edwards?', 'threes', ['Mike Conley', 'Anthony Edwards']]
    print(compare_player_stats(card[3], card[2], df_players, df_opp_per_game, card[0]))
    driver.quit()


if __name__ == "__main__":
    main()
