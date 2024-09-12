from json.decoder import JSONDecodeError
import pandas as pd
from .EuroLeagueData import EuroLeagueData
from .boxscore_data import BoxScoreData
from .utils import get_requests


class PlayByPlay(EuroLeagueData):
    """
    A class for getting the game play-by-play data.

    Args:
        competition (str, optional): The competition code, inherited from the
            `EuroLeagueData` class. Choose one of:
            - 'E' for Euroleague
            - 'U' for Eurocup
            Defaults to "E".
    """

    def get_game_play_by_play_data(
        self,
        season: int,
        gamecode: int
    ) -> pd.DataFrame:
        """
        A function that gets the play-by-play data of a particular game.

        Args:

            season (int): The start year of the season

            gamecode (int): The game-code of the game of interest.
                It can be found on Euroleague's website.

        Returns:

            pd.DataFrame: A dataframe with the play-by-play data of the game.
        """
        url = "https://live.euroleague.net/api/PlaybyPlay"
        params = {
            "gamecode": gamecode,
            "seasoncode": f"{self.competition}{season}"
        }
        r = get_requests(url, params=params)

        try:
            data = r.json()
        except JSONDecodeError:
            raise ValueError(
                f"Game code, {gamecode}, did not return any data.")

        periods = [
            'FirstQuarter', 'SecondQuarter', 'ThirdQuarter', 'ForthQuarter',
            'ExtraTime'
        ]
        all_data = []
        for p, period in enumerate(periods):
            if data[period]:
                df = pd.json_normalize(data[period])
                df["PERIOD"] = p + 1
                all_data.append(df)

        play_by_play_df = pd.concat(all_data).reset_index(drop=True)
        play_by_play_df['CODETEAM'] = play_by_play_df['CODETEAM'].str.strip()
        play_by_play_df['PLAYER_ID'] = play_by_play_df['PLAYER_ID'].str.strip()
        play_by_play_df.insert(0, 'Season', season)
        play_by_play_df.insert(1, 'Gamecode', gamecode)
        return play_by_play_df

    def get_game_play_by_play_data_single_season(
        self,
        season: int
    ) -> pd.DataFrame:
        """
        A function that gets the play-by-play data of *all* games in a single
        season

        Args:

            season (int): The start year of the season

        Returns:

            pd.DataFrame: A dataframe with the play-by-play data of all games
                in a single season
        """
        data_df = self.get_season_data_from_game_data(
            season, self.get_game_play_by_play_data)
        return data_df

    def get_game_play_by_play_data_multiple_seasons(
        self, start_season: int, end_season: int
    ) -> pd.DataFrame:
        """
        A function that gets the play-by-play data of *all* games in a range of
        seasons

        Args:

            start_season (int): The start year of the start season

            end_season (int): The start year of the end season

        Returns:

            pd.DataFrame: A dataframe with the play-by-play data of all games
                in range of seasons
        """
        df = self.get_range_seasons_data(
            start_season, end_season, self.get_game_play_by_play_data)
        return df

    def get_lineups_data(self, season, gamecode):
        """
        Get the teams' lineups and the minute of the game these lineups
        change.

        Args:

            season (int): The start year of the season

            gamecode (int): The game-code of the game of interest.
                It can be found on Euroleague's website.

        Returns:

            pd.DataFrame: A dataframe with the lineups of the teams as they
                change during the game (minute of change is provided)
        """
        # Get the starting line-ups from boxscore data
        boxscoredata = BoxScoreData(competition=self.competition)
        game_bxscr_stats = boxscoredata.get_player_boxscore_stats_data(
            season=season, gamecode=gamecode)

        # find home and away teams
        hm_aw = game_bxscr_stats[["Home", "Team"]].drop_duplicates()
        home_team = hm_aw.loc[hm_aw["Home"] == 1, "Team"].values[0]
        away_team = hm_aw.loc[hm_aw["Home"] == 0, "Team"].values[0]

        starting_five = game_bxscr_stats.loc[
            game_bxscr_stats["IsStarter"] == 1, ["Team", "Player"]
        ]
        starting_five['ID'] = starting_five.groupby('Team').cumcount()

        # Pivot the DataFrame
        starting_five = starting_five.pivot(
            index='ID', columns='Team', values='Player')

        # Reset index if needed
        starting_five.reset_index(drop=True, inplace=True)
        starting_five = starting_five[[home_team, away_team]]
        starting_five_dict = starting_five.to_dict(orient='list')

        # Build the dataframe, whose first row is the starting lineups
        df = pd.DataFrame(
            {
                "Season": [season],
                "Gamecode": [gamecode],
                "PERIOD": [1],
                "MARKERTIME": ["10:00"],
                "MINUTE": [1],
                f"Lineup_{home_team}": [starting_five_dict[home_team]],
                f"Lineup_{away_team}": [starting_five_dict[away_team]],
            }
        )

        # Fetch play-by-play data
        pbp_data = self.get_game_play_by_play_data(
            season=season, gamecode=gamecode)

        # focus on the subs entries
        subs_mask = pbp_data["PLAYTYPE"].isin(["IN", "OUT"])
        subs_data = pbp_data[subs_mask].reset_index(drop=True)

        # pivot to create a dataframe with in/out player by minute and team
        #  side by side, i.e. column-wise.
        subs_data_pivot = subs_data.pivot_table(
            index=["PERIOD", "MINUTE", "MARKERTIME", "CODETEAM"],
            columns="PLAYTYPE",
            values="PLAYER",
            aggfunc=list
        )

        # iterate this dataframe and add/remove players from the line-up list
        n = 0
        home_existing_lineup = starting_five_dict[home_team]
        away_existing_lineup = starting_five_dict[away_team]
        for r, row in subs_data_pivot.iterrows():
            period = r[0]
            minute = r[1]
            time = r[2]
            team = r[3]
            sub_d = dict(zip(row["OUT"], row["IN"]))

            n += 1
            if team == home_team:
                home_new_lineup = [
                    sub_d[u] if u in sub_d else u
                    for u in home_existing_lineup
                ]
                home_existing_lineup = home_new_lineup.copy()

                df.loc[n] = [season, gamecode, period, time,
                             minute, home_new_lineup, away_existing_lineup]
            else:
                away_new_lineup = [
                    sub_d[u] if u in sub_d else u
                    for u in away_existing_lineup
                ]
                away_existing_lineup = away_new_lineup.copy()

                df.loc[n] = [season, gamecode, period, time,
                             minute, home_existing_lineup, away_new_lineup]

        cols = ["Season", "Gamecode", "PERIOD", "MARKERTIME", "MINUTE"]
        # If the two teams made subs in the same minute, these would have
        # been recorded in two seperate lines in the for loop above.
        # Fix the unique minute and keep the latest values of the subs lists.
        line_ups_df = df.drop_duplicates(
            cols, keep="last").reset_index(drop=True)

        return line_ups_df

    def get_pbp_data_with_lineups(self, season, gamecode):
        """
        Get the play-by-play data enrighed with the teams lineups for
        every minute in the PBP data.

        Args:

            season (int): The start year of the season

            gamecode (int): The game-code of the game of interest.
                It can be found on Euroleague's website.

        Returns:

            pd.DataFrame: A dataframe with the play-by-play enriched with
                teams' line ups
        """
        pbp_data = self.get_game_play_by_play_data(
            season=season, gamecode=gamecode)
        line_ups_df = self.get_lineups_data(
            season=season, gamecode=gamecode)
        # hack for consistency
        pbp_data.loc[pbp_data["PLAYTYPE"] == "BP", "MARKERTIME"] = "10:00"

        # cols = ["Season", "Gamecode", "PERIOD", "MARKERTIME", "MINUTE"]
        # lineup_cols = [f"Lineup_{home_team}", f"Lineup_{away_team}"]
        cols = list(line_ups_df.columns[:5])
        lineup_cols = list(line_ups_df.columns[-2:])
        # merge with PBP dataframe
        pbp_lu_data = pbp_data.merge(line_ups_df, on=cols, how="left")
        # update the starting lineups
        pbp_lu_data.loc[0, lineup_cols] = line_ups_df.loc[0, lineup_cols]
        # forward fill the lineups until a lineup entry changes
        pbp_lu_data[lineup_cols] = pbp_lu_data[lineup_cols].ffill()
        # fix hack
        pbp_lu_data.loc[pbp_lu_data["PLAYTYPE"] == "BP", "MARKERTIME"] = ""

        return pbp_lu_data
