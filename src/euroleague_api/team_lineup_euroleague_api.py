import pandas as pd
import numpy as np
from euroleague_api.play_by_play_data import PlayByPlay
from euroleague_api.boxscore_data import BoxScoreData

def pbp_data_with_lineups(season, game_code):
    
    # Getting pbp for the match
    pbp = PlayByPlay()
    pbp_data = pbp.get_game_play_by_play_data(season=season, gamecode=game_code)
    pbp_data = pbp_data.reset_index(drop=True)

    # Getting starting five
    boxscoredata = BoxScoreData()
    game_bxscr_stats = boxscoredata.get_player_boxscore_stats_data(season=season, gamecode=game_code)

    starting_five = game_bxscr_stats.loc[game_bxscr_stats["IsStarter"] == 1, ["Team", "Player"]]
    starting_five['ID'] = starting_five.groupby('Team').cumcount()
    starting_five = starting_five.pivot(index='ID', columns='Team', values='Player')
    starting_five.reset_index(drop=True, inplace=True)

    # Filling start of the match with starters
    on_court_mask1 = ['Team_A1', 'Team_A2', 'Team_A3', 'Team_A4', 'Team_A5']
    on_court_mask2 = ['Team_B1', 'Team_B2', 'Team_B3', 'Team_B4', 'Team_B5']

    # Creating player columns
    on_court_cols = on_court_mask1 + on_court_mask2
    pbp_data[on_court_cols] = np.nan

    pbp_data.loc[0, on_court_mask1] = starting_five.iloc[:, 0].tolist()
    pbp_data.loc[0, on_court_mask2] = starting_five.iloc[:, 1].tolist()

    # Capturing subs and replacing player columns with players who substitute in
    players = pbp_data.loc[0, on_court_cols]

    for idx,row in pbp_data.loc[pbp_data['PLAYTYPE'].isin(['IN', 'OUT']), :].iterrows(): # looping through IN & OUTs of the game
        if row['PLAYTYPE'] == 'IN':
            sub_time = row['MARKERTIME']
            sub_min = row['MINUTE']
            sub_team = row['TEAM']
            all_subs = pbp_data.loc[(pbp_data.MINUTE == sub_min) & (pbp_data['MARKERTIME'] == sub_time) & (pbp_data.PLAYTYPE.isin(['IN', 'OUT'])), :].sort_values(by='PLAYTYPE')

            if pd.isnull(pbp_data.loc[max(all_subs.index), 'Team_A1']): # if I haven't made any replacement yet
                subs_team1 = all_subs.loc[all_subs['TEAM'] == sub_team, :]
                subs_team2 = all_subs.loc[all_subs['TEAM'] != sub_team, :]
                in_players_1 = []
                out_players_1 = []
                for i in subs_team1.index: # capturing every sub made by the first team at that particular time in the match
                    if subs_team1.loc[i, 'PLAYTYPE'] == 'IN':
                        tmp_in_player = subs_team1.loc[i, 'PLAYER']
                        in_players_1.append(tmp_in_player)
                    elif subs_team1.loc[i, 'PLAYTYPE'] == 'OUT':
                        tmp_out_player = subs_team1.loc[i, 'PLAYER']
                        out_players_1.append(tmp_out_player)
                
                in_players_2 = []
                out_players_2 = []
                for i in subs_team2.index: # capturing every sub made by the second team at that particular time in the match
                    if subs_team2.loc[i, 'PLAYTYPE'] == 'IN':
                        tmp_in_player = subs_team2.loc[i, 'PLAYER']
                        in_players_2.append(tmp_in_player)
                    elif subs_team2.loc[i, 'PLAYTYPE'] == 'OUT':
                        tmp_out_player = subs_team2.loc[i, 'PLAYER']
                        out_players_2.append(tmp_out_player)
                
                subs_dict = {} # empty dictionary to create key-value pairs for the subs

                all_ins = in_players_1 + in_players_2 # every player who subs in
                all_outs = out_players_1 + out_players_2 # every player who subs out

                for out_p, in_p in zip(all_outs, all_ins):
                    subs_dict[out_p] = in_p # creating the dictionary appropriately. Player who subs out becomes the key while the player who subs in becomes the value
                
                for key in subs_dict.keys(): # make the subs and hold them in the players variable
                    for j, player in enumerate(players):
                        if key == player:
                            players[j] = subs_dict[key]
                        else:
                            continue
                
                pbp_data.loc[max(all_subs.index), on_court_cols] = players # replace them in the actual dataframe
            
            else:
                pass
    
    pbp_data.loc[:, on_court_cols] = pbp_data.loc[:, on_court_cols].fillna(method='ffill') # filling every play

    return pbp_data # returns the dataframe

df = pbp_data_with_lineups(2023, 302)

df.loc[:, [col for col in df.columns if col.startswith('Team')]]