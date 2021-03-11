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
import scrape_data
from auto_run import auto_compare_players, auto_compare_teams


def add_players_stat_to_cards(cards, player_list):
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


def manual_entry(cards, players_df, opp_df, team_df, player_list, vegas):
    stat_list = ['assists', 'points', 'rebounds', '3 pointers']

    player = input("Player's full name: ")
    if player.lower() == 'q':
        prompt_user(cards, player_list, players_df, team_df, opp_df, vegas)
    if player not in players_df.index:
        print('Use full player name\n')
        manual_entry(cards, players_df, team_df, opp_df, player_list, vegas)

    stat = input("Stat in question: ")
    if stat.lower() == 'q':
        prompt_user(players_df, team_df, opp_df, player_list, vegas)
    if stat.lower() not in stat_list:
        print("Viable stats are 'assists', 'points', 'rebounds', '3 pointers'\n")
        manual_entry(cards, players_df, team_df, opp_df, player_list, vegas)

    opp_team = input("Opposing team: ")
    if opp_team.lower() == 'q':
        prompt_user(players_df, team_df, opp_df, player_list, vegas)
    if opp_team not in opp_df.index:
        print("Needs full location and team name (Ex: 'Minnesota Timberwolves')\n")
        manual_entry(cards, players_df, team_df, opp_df, player_list, vegas)

    player_question_output = ''
    if stat.lower() == '3 pointers':
        player_threes = float(players_df.loc[player][9])
        defense_threes = float(opp_df.loc[f'{opp_team}'][7])
        league_threes_avg = float(opp_df.loc['League Average'][7])
        predicted_threes = round(player_threes * (defense_threes / league_threes_avg), 1)

        player_question_output += (f'   {player}: {player_threes} 3s per game\n')
        player_question_output += (f'   {player}: {predicted_threes} weighted against {opp_team}\n')

    elif stat.lower() == 'assists':
        player_assists = float(players_df.loc[player][22])
        def_assists = float(opp_df.loc[f'{opp_team}'][17])
        league_assists_avg = float(opp_df.loc['League Average'][17])
        predicted_assists = round(player_assists * (def_assists / league_assists_avg), 1)

        player_question_output += (f'   {player}: {player_assists} assists per game\n')
        player_question_output += (f'   {player}: {predicted_assists} weighted against {opp_team}\n')

    elif stat.lower() == 'rebounds':
        player_rebounds = float(players_df.loc[player][21])
        def_rebounds = float(opp_df.loc[f'{opp_team}'][16])
        league_rebounds_avg = float(opp_df.loc['League Average'][16])
        predicted_rebounds = round(player_rebounds * (def_rebounds / league_rebounds_avg), 1)

        player_question_output += (f'   {player}: {player_rebounds} rebounds per game\n')
        player_question_output += (f'   {player}: {predicted_rebounds} weighted against {opp_team}\n')

    elif stat.lower() == 'points':
        points_from_two = float(players_df.loc[player][12]) * 2
        points_from_three = float(players_df.loc[player][9]) * 3
        points_from_ft = float(players_df.loc[player][16])

        defense_twos = float(opp_df.loc[f'{opp_team}'][10])
        defense_threes = float(opp_df.loc[f'{opp_team}'][7])

        league_twos_avg = float(opp_df.loc['League Average'][10])
        league_threes_avg = float(opp_df.loc['League Average'][7])

        predicted_points = round(points_from_two * (defense_twos/league_twos_avg) + points_from_three * (defense_threes/league_threes_avg) + points_from_ft, 1)

        player_question_output += (f'   {player}: {players_df.loc[player][27]}ppg\n')
        player_question_output += (f'   {player}: {predicted_points} weighted against {opp_team}\n')
    else:
        player_question_output += 'Error in players stats'
    print(player_question_output)

    run_prompt = input('Another player? Y/N (\'q\' for quit)\n')
    if run_prompt.lower() == 'y':
        manual_entry(cards, players_df, opp_df, team_df, player_list, vegas)
    elif run_prompt.lower() == 'q':
        print('Exiting...')
        exit()
    else:
        exit()


def prompt_user(cards, player_list, players_df, team_df, opp_df, vegas):
    user_method = input('Manual or Auto? (\'q\' for quit)\n')
    if user_method.lower() == 'manual':
        pass
        manual_entry(cards, players_df, opp_df, team_df, player_list, vegas)
    elif user_method.lower() == 'auto':
        add_players_stat_to_cards(cards, player_list)

        for i, card in enumerate(cards):
            if 'team' in card[1]:
                print(f'Question {i + 1}: {card[1]}, {card[0][0]} or {card[0][1]}')
                print(auto_compare_teams(card[0][0], card[0][1], card[2], team_df, opp_df,
                                         vegas)) # First team, second team, stat in question
            else:
                print(f'Question {i + 1}: {card[1]}')
                print(auto_compare_players(card[3], card[0], card[2], players_df, opp_df)) # Players, teams, stat in question

        prompt_user(cards, player_list, players_df, team_df, opp_df, vegas)


def main():
    print("Please wait, scraping data from web and organizing into dataframes")
    print("This can take a minute")
    driver = webdriver.Firefox()
    driver.implicitly_wait(4)
    cards = scrape_data.curr_pickem_qs(driver)
    player_list = scrape_data.retrieve_player_list(driver)
    players_df = scrape_data.create_players_df(driver)
    team_df = scrape_data.create_team_df(driver)
    opp_df = scrape_data.create_opp_df(driver)
    vegas = scrape_data.retrieve_vegas_odds(driver)
    driver.quit()
    prompt_user(cards, player_list, players_df, team_df, opp_df, vegas)


if __name__ == "__main__":
    main()
