from teams_dict import convert_to_abbrev


def auto_compare_teams(team_1, team_2, stat, team_df, opp_df, adv_df, vegas):
    output = ''  # initialize
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

    elif stat == 'fg':
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

    elif stat == 'win':
        team_1_stat = float(adv_df.loc[f'{team_1}'][7])
        team_2_stat = float(adv_df.loc[f'{team_2}'][7])
        team_1_netrtg = float(adv_df.loc[f'{team_1}'][10])
        team_2_netrtg = float(adv_df.loc[f'{team_2}'][10])

        output += f'   {team_1}: {team_1_stat} Simple Rating System\n'
        output += f'   {team_2}: {team_2_stat} Simple Rating System\n'
        output += f'   {team_1}: {team_1_netrtg} Net Rating\n'
        output += f'   {team_2}: {team_2_netrtg} Net Rating\n'

        output += '\n   Current Vegas odds:\n'
        if vegas == {}:
            print('   Vegas odds unavailable\n')
        else:
            output += f'   {team_1}: {str(vegas.get(team_1))}\n'
            output += f'   {team_2}: {str(vegas.get(team_2))}\n'


    else:
        output = 'Error in get_team_stat'

    return output


def auto_compare_players(players, teams, stat, players_df, opp_df):
    player_question_output = ''
    teams_abbr = []

    # Get abbreviated form of team for Basketball Reference player stats
    for team in teams:
        teams_abbr.append(convert_to_abbrev[team])

    for player in players:
        # Given the two teams, which one is the player not on?
        opp_team = None
        for team in teams_abbr:
            if players_df.loc[player][2] != team:
                opp_team = team
        for team, abbr in convert_to_abbrev.items():
            if abbr == opp_team:
                opp_team = team

        if stat.lower() == '3 pointers':
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

    return player_question_output
