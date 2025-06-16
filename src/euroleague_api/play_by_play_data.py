import logging
from json.decoder import JSONDecodeError
import pandas as pd
import numpy as np
from .EuroLeagueData import EuroLeagueData
from .boxscore_data import BoxScoreData
from .utils import get_requests

logger = logging.getLogger(__name__)


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
        except JSONDecodeError as exc:
            raise ValueError(
                f"Game code, {gamecode}, season {season}, "
                "did not return any data."
            ) from exc

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

        pbp_df = pd.concat(all_data).reset_index(drop=True)
        pbp_df['CODETEAM'] = pbp_df['CODETEAM'].str.strip()
        pbp_df['PLAYER_ID'] = pbp_df['PLAYER_ID'].str.strip()
        pbp_df["PLAYTYPE"] = pbp_df["PLAYTYPE"].str.strip()
        pbp_df["MARKERTIME"] = pbp_df["MARKERTIME"].str.strip()
        pbp_df.insert(0, 'Season', season)
        pbp_df.insert(1, 'Gamecode', gamecode)
        return pbp_df

    def get_play_by_play_data_round(
        self,
        season: int,
        round_number: int
    ) -> pd.DataFrame:
        """
        A function that gets the play-by-play data of *all* games in a single
        round

        Args:
            season (int): The start year of the season
            round_number (int): The round of the season

        Returns:
            pd.DataFrame: A dataframe with the play-by-play data of all games
                in a single round_number
        """
        df = self.get_round_data_from_game_data(
            season, round_number, self.get_game_play_by_play_data)
        return df

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

    def get_pbp_data_with_lineups(
        self,
        season,
        gamecode,
        validate=True
    ) -> pd.DataFrame:
        """
        Get the play-by-play (PBP) data enriched with the teams' lineups for
        every action in the PBP data.

        There are three cases where the player in the corresponding row
        (action) is not part of the lineup:

            1. When the player is subbed "OUT", the assigned lineup does not
            contain player name. Since this is reasonable, the value of the
            `validate_on_court_player` indicator is set to `True`.

            2. A player passes on to a teamate, who draws a shooting foul. If
            the passer is subbed before the first free throw and the first free
            throw is made then the subbed player is given an assist. However,
            the player is not in the extracted lineup because he has already
            been subbed. The value of the `validate_on_court_player`
            indicator is set to `False`. We don't fix the lineup, because it
            breaks the lineup continuinity. It is a quirk of the data
            collection andrecording.

            3. There are a few instances where a sub is recorded many seconds
            and actions since it actually happened. This causes issues, such
            as a player records an actions, such as a rebound, but he comes
            on the court (according to the data) many seconds after. This has
            been validated by watching theactual footage of the game. This
            requires a lot of manual work, which is beyond the score of this
            library. It is another quirk of the datacollection and recording,
            hence the value of the `validate_on_court_player` indicator is set
            to `False`.

        Args:

            season (int): The start year of the season

            gamecode (int): The game-code of the game of interest.
                It can be found on Euroleague's website.

            validate (bool, optional): A bool indicator whether to enrich the
                dataframe with two extra columns, which validate the validity
                and consistency of the extracted lineup. Defaults to True.

        Returns:

            pd.DataFrame: A dataframe with the play-by-play enriched with
                teams' lineups
        """
        def process_sub(five, player, sub_type):
            opp_sub_type = "OUT" if sub_type == "IN" else "IN"
            potential_indx = (
                pbp_data.loc[idx + 1:].index[
                    (pbp_data.loc[idx + 1:, "PLAYTYPE"] == opp_sub_type)
                ]
            )
            potential_nops = (
                set(potential_indx).difference(processed_idxs)
            )
            matching_idx = min(potential_nops)
            processed_idxs.append(idx)
            processed_idxs.append(matching_idx)
            matching_row = pbp_data.loc[matching_idx]
            invalid_mask = (
                (matching_row["PLAYTYPE"] != opp_sub_type) or
                (matching_row["CODETEAM"] != team) or
                (matching_row["MARKERTIME"] != markertime)
            )
            if invalid_mask:
                logger.warning(
                    f"Something went wrong for gamecode {gamecode} at sub "
                    f"index {idx} with matching sub index {matching_idx}"
                )
            player_sub = matching_row["PLAYER"].replace(" ,", ",")
            player_in = player if sub_type == "IN" else player_sub
            player_out = player_sub if sub_type == "IN" else player
            if player_in == player_out:
                # there are instance where the same player is subbed in and out
                return five
            else:
                pindx = five.index(player_out)
                five = five[:pindx] + [player_in] + five[pindx + 1:]
                return five

        def validate_player(x, col1, col2):
            flag = False
            if (x["PLAYER"] is not None) and (x["PLAYTYPE"] != "OUT"):
                if x["PLAYER"].replace(" ,", ",") in (x[col1] + x[col2]):
                    flag = True
            else:
                flag = True
            return flag

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

        # Fetch play-by-play data
        pbp_data = self.get_game_play_by_play_data(
            season=season, gamecode=gamecode)

        # Asign the starting lineups to the first entry of the PBP data.
        pbp_data["Lineup_A"] = None
        pbp_data["Lineup_B"] = None
        pbp_data.at[0, "Lineup_A"] = starting_five_dict[home_team]
        pbp_data.at[0, "Lineup_B"] = starting_five_dict[away_team]
        pbp_data["IsHomeTeam"] = np.where(
            pbp_data["CODETEAM"] == home_team, True,
            np.where(pbp_data["CODETEAM"] == away_team,
                     False, None)  # type: ignore
        )

        # start processing the sub entries, row by row.
        processed_idxs: list = []
        current_five_home = starting_five_dict[home_team].copy()
        current_five_away = starting_five_dict[away_team].copy()
        for idx, row in pbp_data.iterrows():
            playtype = row["PLAYTYPE"]
            # there are rare instances of an extra space in player name
            player = (
                row["PLAYER"] if row["PLAYER"] is None
                else row["PLAYER"].replace(" ,", ",")
            )
            team = row["CODETEAM"]
            markertime = row["MARKERTIME"]
            if team != "":
                is_home = home_team == team
                five = current_five_home if is_home else current_five_away
                if (playtype == "OUT") and (idx not in processed_idxs):
                    five = process_sub(five, player, playtype)
                elif (playtype == "IN") and (idx not in processed_idxs):
                    five = process_sub(five, player, playtype)
                if is_home:
                    current_five_home = five
                else:
                    current_five_away = five

            pbp_data.at[idx, "Lineup_A"] = current_five_home
            pbp_data.at[idx, "Lineup_B"] = current_five_away

        if validate:
            lu_cols = [u for u in pbp_data.columns if u.startswith("Lineup_")]
            pbp_data["validate_on_court_player"] = pbp_data.apply(
                lambda x: validate_player(x, lu_cols[0], lu_cols[1]),
                axis=1
            )
        return pbp_data

    def get_pbp_data_with_lineups_round(
        self,
        season: int,
        round_number: int
    ) -> pd.DataFrame:
        """
        A function that gets the play-by-play with lineups data of *all* games
        in a single round

        Args:
            season (int): The start year of the season
            round_number (int): The round of the season

        Returns:
            pd.DataFrame: A dataframe with the play-by-play data with lineups
                of all games in a single round
        """
        df = self.get_round_data_from_game_data(
            season, round_number, self.get_pbp_data_with_lineups)
        return df

    def get_pbp_data_with_lineups_single_season(
        self,
        season: int
    ) -> pd.DataFrame:
        """
        A function that gets the play-by-play data enriched with team lineups
        of *all* games in a single season

        Args:

            season (int): The start year of the season

        Returns:

            pd.DataFrame: A dataframe with the play-by-play data of all games
                in a single season
        """
        data_df = self.get_season_data_from_game_data(
            season, self.get_pbp_data_with_lineups)
        return data_df

    def get_pbp_data_with_lineups_multiple_seasons(
        self, start_season: int, end_season: int
    ) -> pd.DataFrame:
        """
        A function that gets the play-by-play data enriched with team lineups
        of *all* games in a range of seasons

        Args:

            start_season (int): The start year of the start season

            end_season (int): The start year of the end season

        Returns:

            pd.DataFrame: A dataframe with the play-by-play data of all games
                in range of seasons
        """
        df = self.get_range_seasons_data(
            start_season, end_season, self.get_pbp_data_with_lineups)
        return df
