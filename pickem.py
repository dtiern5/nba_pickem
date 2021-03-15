from selenium import webdriver
from find_stat import find_stat
import scrape_data
from auto_run import auto_compare_players, auto_compare_teams
from teams_dict import convert_to_abbrev


def manual_team(cards, players_df, opp_df, team_df, player_list, adv_df, vegas, stat_list):

    team_1 = input('First team: ').upper()
    if team_1.lower() == 'q':
        prompt_user(cards, player_list, players_df, team_df, opp_df, adv_df, vegas)
    if team_1.lower() == 'ls':
        print('\nTeams List:')
        for item in convert_to_abbrev.items():
            print(item)
        print('\n')
        manual_team(cards, players_df, team_df, opp_df, player_list, adv_df, vegas, stat_list)
    if team_1 not in convert_to_abbrev.values():
        print('Unrecognized team\n')
        manual_team(cards, players_df, team_df, opp_df, player_list, adv_df, vegas, stat_list)

    team_2 = input('Second team: ').upper()
    if team_2.lower() == 'q':
        prompt_user(cards, player_list, players_df, team_df, opp_df, adv_df, vegas)
    if team_1.lower() == 'ls':
        print('\nTeams List:')
        for item in convert_to_abbrev.items():
            print(item)
        manual_team(cards, players_df, team_df, opp_df, player_list, adv_df, vegas, stat_list)
    if team_2 not in convert_to_abbrev.values():
        print('Unrecognized team\n')
        manual_team(cards, players_df, team_df, opp_df, player_list, adv_df, vegas, stat_list)

    stat = input("Stat to compare: ").lower()
    if stat == 'q':
        prompt_user(cards, player_list, players_df, team_df, opp_df, adv_df, vegas)
    if stat not in stat_list:
        print('Unrecognized stat\n')
        manual_team(cards, players_df, team_df, opp_df, player_list, adv_df, vegas, stat_list)

    # Convert abbreviated team names to full name for Basketball Reference table
    for key, value in convert_to_abbrev.items():
        if team_1 == value:
            team_1 = key
        if team_2 == value:
            team_2 = key

    output = ''
    if stat == 'rebounds':
        team_1_stat = float(team_df.loc[f'{team_1}'][16])
        team_1_opp_stat = float(opp_df.loc[f'{team_1}'][16])
        team_2_stat = float(team_df.loc[f'{team_2}'][16])
        team_2_opp_stat = float(opp_df.loc[f'{team_2}'][16])
        league_avg_stat = float(team_df.loc[f'League Average'][16])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        output += f'   {team_1}: {team_1_stat} rebounds per game\n' \
                  f'   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        output += f'   {team_2}: {team_2_stat} rebounds per game\n' \
                  f'   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'assists':
        team_1_stat = float(team_df.loc[f'{team_1}'][17])
        team_1_opp_stat = float(opp_df.loc[f'{team_1}'][17])
        team_2_stat = float(team_df.loc[f'{team_2}'][17])
        team_2_opp_stat = float(opp_df.loc[f'{team_2}'][17])
        league_avg_stat = float(team_df.loc[f'League Average'][17])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        output += f'   {team_1}: {team_1_stat} assists per game\n' \
                  f'   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        output += f'   {team_2}: {team_2_stat} assists per game\n' \
                  f'   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'steals':
        team_1_stat = float(team_df.loc[f'{team_1}'][18])
        team_1_opp_stat = float(opp_df.loc[f'{team_1}'][18])
        team_2_stat = float(team_df.loc[f'{team_2}'][18])
        team_2_opp_stat = float(opp_df.loc[f'{team_2}'][18])
        league_avg_stat = float(team_df.loc[f'League Average'][18])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        output += f'   {team_1}: {team_1_stat} steals per game\n' \
                  f'   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        output += f'   {team_2}: {team_2_stat} steals per game\n' \
                  f'   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'blocks':
        team_1_stat = float(team_df.loc[f'{team_1}'][19])
        team_1_opp_stat = float(opp_df.loc[f'{team_1}'][19])
        team_2_stat = float(team_df.loc[f'{team_2}'][19])
        team_2_opp_stat = float(opp_df.loc[f'{team_2}'][19])
        league_avg_stat = float(team_df.loc[f'League Average'][19])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        output += f'   {team_1}: {team_1_stat} blocks per game\n' \
                  f'   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        output += f'   {team_2}: {team_2_stat} blocks per game\n' \
                  f'   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'field goal':
        team_1_stat = float(team_df.loc[f'{team_1}'][4])
        team_1_opp_stat = float(opp_df.loc[f'{team_1}'][4])
        team_2_stat = float(team_df.loc[f'{team_2}'][4])
        team_2_opp_stat = float(opp_df.loc[f'{team_2}'][4])
        league_avg_stat = float(team_df.loc[f'League Average'][4])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 3)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 3)

        output += f'   {team_1}: {team_1_stat} FG% per game\n' \
                  f'   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        output += f'   {team_2}: {team_2_stat} FG% per game\n' \
                  f'   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == '3 pointers':
        team_1_stat = float(team_df.loc[f'{team_1}'][5])
        team_1_opp_stat = float(opp_df.loc[f'{team_1}'][5])
        team_2_stat = float(team_df.loc[f'{team_2}'][5])
        team_2_opp_stat = float(opp_df.loc[f'{team_2}'][5])
        league_avg_stat = float(team_df.loc[f'League Average'][5])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        output += f'   {team_1}: {team_1_stat} 3 pointers per game\n' \
                  f'   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        output += f'   {team_2}: {team_2_stat} 3 pointers per game\n' \
                  f'   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'free throws':
        team_1_stat = float(team_df.loc[f'{team_1}'][11])
        team_1_opp_stat = float(opp_df.loc[f'{team_1}'][11])
        team_2_stat = float(team_df.loc[f'{team_2}'][11])
        team_2_opp_stat = float(opp_df.loc[f'{team_2}'][11])
        league_avg_stat = float(team_df.loc[f'League Average'][11])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        output += f'   {team_1}: {team_1_stat} free throws per game\n' \
                  f'   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        output += f'   {team_2}: {team_2_stat} free throws per game\n' \
                  f'   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'points':
        team_1_stat = float(team_df.loc[f'{team_1}'][22])
        team_1_opp_stat = float(opp_df.loc[f'{team_1}'][22])
        team_2_stat = float(team_df.loc[f'{team_2}'][22])
        team_2_opp_stat = float(opp_df.loc[f'{team_2}'][22])
        league_avg_stat = float(team_df.loc[f'League Average'][22])

        team_1_prediction = round(team_1_stat * (team_2_opp_stat / league_avg_stat), 1)
        team_2_prediction = round(team_2_stat * (team_1_opp_stat / league_avg_stat), 1)

        output += f'   {team_1}: {team_1_stat} points per game\n' \
                  f'   {team_1}: {team_1_prediction} weighted against {team_2}\n'
        output += f'   {team_2}: {team_2_stat} points per game\n' \
                  f'   {team_2}: {team_2_prediction} weighted against {team_1}\n'

    elif stat == 'winner':
        team_1_stat = float(adv_df.loc[f'{team_1}'][7])
        team_2_stat = float(adv_df.loc[f'{team_2}'][7])
        team_1_netrtg = float(adv_df.loc[f'{team_1}'][10])
        team_2_netrtg = float(adv_df.loc[f'{team_2}'][10])

        output += f'   {team_1}: {team_1_stat} Simple Rating System\n'
        output += f'   {team_1}: {team_1_netrtg} Net Rating\n'
        output += f'   {team_2}: {team_2_stat} Simple Rating System\n'
        output += f'   {team_2}: {team_2_netrtg} Net Rating\n'

    print(output)

    run_prompt = input('Another team question? Y/N\n')
    if run_prompt.lower() == 'y':
        manual_team(cards, players_df, opp_df, team_df, player_list, adv_df, vegas, stat_list)
    else:
        prompt_user(cards, player_list, players_df, team_df, opp_df, adv_df, vegas)


def manual_player(cards, players_df, opp_df, team_df, player_list, adv_df, vegas, stat_list):

    player = input("Player's full name: ")
    if player.lower() == 'q':
        prompt_user(cards, player_list, players_df, team_df, opp_df, adv_df, vegas)
    if player.lower() == 'ls':
        print('\nTeams List:')
        for item in convert_to_abbrev.items():
            print(item)
        manual_player(cards, players_df, team_df, opp_df, player_list, adv_df, vegas, stat_list)
    if player not in players_df.index:
        print('Unrecognized player\n')
        manual_player(cards, players_df, team_df, opp_df, player_list, adv_df, vegas, stat_list)

    stat = input("Stat in question: ").lower()
    if stat == 'q':
        prompt_user(cards, player_list, players_df, team_df, opp_df, adv_df, vegas)
    if stat == 'ls':
        print('\nTeams List:')
        for item in convert_to_abbrev.items():
            print(item)
        print('\n')
        manual_player(cards, players_df, team_df, opp_df, player_list, adv_df, vegas, stat_list)
    if stat not in stat_list:
        print('Unrecognized stat\n')
        manual_player(cards, players_df, team_df, opp_df, player_list, adv_df, vegas, stat_list)

    opp_team = input("Opposing team: ").upper()
    if opp_team.lower() == 'q':
        prompt_user(cards, player_list, players_df, team_df, opp_df, adv_df, vegas)
    if opp_team.lower() == 'ls':
        print('\nTeams List:')
        for item in convert_to_abbrev.items():
            print(item)
        print('\n')
        manual_player(cards, players_df, team_df, opp_df, player_list, adv_df, vegas, stat_list)
    if opp_team not in convert_to_abbrev.values():
        print('Unrecognized team\n')
        manual_player(cards, players_df, team_df, opp_df, player_list, adv_df, vegas, stat_list)

    # Convert abbreviated team name to full name for Basketball Reference table
    for key, value in convert_to_abbrev.items():
        if opp_team == value:
            opp_team = key

    player_question_output = ''
    if stat == '3 pointers':
        player_threes = float(players_df.loc[player][9])
        defense_threes = float(opp_df.loc[f'{opp_team}'][7])
        league_threes_avg = float(opp_df.loc['League Average'][7])
        predicted_threes = round(player_threes * (defense_threes / league_threes_avg), 1)

        player_question_output += f'   {player}: {player_threes} 3s per game\n'
        player_question_output += f'   {player}: {predicted_threes} weighted against {opp_team}\n'

    elif stat == 'assists':
        player_assists = float(players_df.loc[player][22])
        def_assists = float(opp_df.loc[f'{opp_team}'][17])
        league_assists_avg = float(opp_df.loc['League Average'][17])
        predicted_assists = round(player_assists * (def_assists / league_assists_avg), 1)

        player_question_output += f'   {player}: {player_assists} assists per game\n'
        player_question_output += f'   {player}: {predicted_assists} weighted against {opp_team}\n'

    elif stat == 'rebounds':
        player_rebounds = float(players_df.loc[player][21])
        def_rebounds = float(opp_df.loc[f'{opp_team}'][16])
        league_rebounds_avg = float(opp_df.loc['League Average'][16])
        predicted_rebounds = round(player_rebounds * (def_rebounds / league_rebounds_avg), 1)

        player_question_output += f'   {player}: {player_rebounds} rebounds per game\n'
        player_question_output += f'   {player}: {predicted_rebounds} weighted against {opp_team}\n'

    elif stat == 'blocks':
        player_blocks = float(players_df.loc[player][24])
        defense_blocks = float(opp_df.loc[f'{opp_team}'][19])
        league_blocks_avg = float(opp_df.loc['League Average'][19])
        predicted_blocks = round(player_blocks * (defense_blocks / league_blocks_avg), 1)

        player_question_output += f'   {player}: {player_blocks} blocks per game\n'
        player_question_output += f'   {player}: {predicted_blocks} weighted against {opp_team}\n'

    elif stat == 'field goal':
        player_fg = float(players_df.loc[player][8])
        defense_fg = float(opp_df.loc[f'{opp_team}'][4])
        league_fg_avg = float(opp_df.loc['League Average'][4])
        predicted_fg = round(player_fg * (defense_fg / league_fg_avg), 3)

        player_question_output += f'   {player}: {player_fg} FG% per game\n'
        player_question_output += f'   {player}: {predicted_fg} weighted against {opp_team}\n'

    elif stat == 'free throws':
        player_ft = float(players_df.loc[player][16])
        defense_ft = float(opp_df.loc[f'{opp_team}'][11])
        league_ft_avg = float(opp_df.loc['League Average'][11])
        predicted_ft = round(player_ft * (defense_ft / league_ft_avg), 1)

        player_question_output += f'   {player}: {player_ft} free throws per game\n'
        player_question_output += f'   {player}: {predicted_ft} weighted against {opp_team}\n'

    elif stat == 'steals':
        player_steals = float(players_df.loc[player][23])
        defense_steals = float(opp_df.loc[f'{opp_team}'][18])
        league_steals_avg = float(opp_df.loc['League Average'][18])
        predicted_steals = round(player_steals * (defense_steals / league_steals_avg), 1)

        player_question_output += f'   {player}: {player_steals} steals per game\n'
        player_question_output += f'   {player}: {predicted_steals} weighted against {opp_team}\n'

    elif stat == 'points':
        points_from_two = float(players_df.loc[player][12]) * 2
        points_from_three = float(players_df.loc[player][9]) * 3
        points_from_ft = float(players_df.loc[player][16])

        defense_twos = float(opp_df.loc[f'{opp_team}'][10])
        defense_threes = float(opp_df.loc[f'{opp_team}'][7])

        league_twos_avg = float(opp_df.loc['League Average'][10])
        league_threes_avg = float(opp_df.loc['League Average'][7])

        predicted_points = round(points_from_two * (defense_twos / league_twos_avg) + points_from_three * (
                defense_threes / league_threes_avg) + points_from_ft, 1)

        player_question_output += f'   {player}: {players_df.loc[player][27]}ppg\n'
        player_question_output += f'   {player}: {predicted_points} weighted against {opp_team}\n'
    else:
        player_question_output += 'Error in players stats'
    print(player_question_output)

    run_prompt = input('Another player? Y/N\n')
    if run_prompt.lower() == 'y':
        manual_player(cards, players_df, opp_df, team_df, player_list, adv_df, vegas, stat_list)
    else:
        prompt_user(cards, player_list, players_df, team_df, opp_df, adv_df, vegas)


# Function adds to the card: the players in question and the specific stat in question
def cards_add_info(cards, player_list):
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


def prompt_user(cards, player_list, players_df, team_df, opp_df, adv_df, vegas):
    user_method = input("'Manual' or 'Auto'? (\'q\' for quit): ").lower()

    if user_method == 'manual':
        team_or_player = input("'Team' or 'player' question? ").lower()
        if team_or_player.lower() == 'player':
            stat_list = ['3 pointers', 'assists', 'blocks', 'field goal', 'free throws', 'points', 'rebounds', 'steals']

            print("\nUse abbreviated team names (e.g. 'BRK', 'CHO', 'NOP')")
            print("Type 'ls' to see acceptable team names")
            print(f'Eligible stats: {stat_list}')
            print("Type 'q' to quit\n")
            manual_player(cards, players_df, opp_df, team_df, player_list, adv_df, vegas, stat_list)

        elif team_or_player == 'team':
            stat_list = ['3 pointers', 'assists', 'blocks', 'field goal', 'free throws',
                         'points', 'rebounds', 'steals', 'winner']

            print("\nUse abbreviated team names (e.g. 'BRK', 'CHO', 'NOP')")
            print("Type 'ls' to see acceptable team names")
            print(f'Eligible stats: {stat_list}')
            print("Type 'q' to quit\n")
            manual_team(cards, players_df, opp_df, team_df, player_list, adv_df, vegas, stat_list)

        else:
            prompt_user(cards, player_list, players_df, team_df, opp_df, adv_df, vegas)

    elif user_method == 'auto':
        # adds card[2] for stat involved in question, and card[3] for list of either one or two players
        # card format: [[team_1, team_2], 'Pickem Question', 'stat' from question, [player_1, player_2]]
        cards_add_info(cards, player_list)
        print('\n')
        for i, card in enumerate(cards):
            if 'team' in card[1]:
                print(f'Question {i + 1}: {card[1]}, {card[0][0]} or {card[0][1]}')
                print(auto_compare_teams(card[0][0], card[0][1], card[2], team_df, opp_df, adv_df,
                                         vegas))  # First team, second team, stat in question
            else:
                print(f'Question {i + 1}: {card[1]}')
                print(auto_compare_players(card[3], card[0], card[2], players_df,
                                           opp_df))  # Players, teams, stat in question

        prompt_user(cards, player_list, players_df, team_df, opp_df, adv_df, vegas)

    elif user_method == 'q':
        quit()

    else:
        print('Not a valid input')
        prompt_user(cards, player_list, players_df, team_df, opp_df, adv_df, vegas)


def main():
    print("Please wait, preparing data...")
    driver = webdriver.Firefox()
    driver.implicitly_wait(4)
    # Each 'card' is information for each question [team1, team2], question]
    cards = scrape_data.curr_pickem_qs(driver)
    player_list = scrape_data.retrieve_player_list(driver)
    players_df = scrape_data.create_players_df(driver)
    team_df = scrape_data.create_team_df(driver)
    opp_df = scrape_data.create_opp_df(driver)
    adv_df = scrape_data.create_adv_df(driver)
    vegas = scrape_data.retrieve_vegas_odds(driver)
    driver.quit()
    prompt_user(cards, player_list, players_df, team_df, opp_df, adv_df, vegas)


if __name__ == "__main__":
    main()
