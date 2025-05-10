from typing import Optional
import pandas as pd
import numpy as np
from .EuroLeagueData import EuroLeagueData
from .boxscore_data import BoxScoreData
from .play_by_play_data import PlayByPlay
from .utils import raise_error, get_requests


class TeamStats(EuroLeagueData):
    """
    A class for getting team-level stats and data.

    Args:
        competition (str, optional): The competition code, inherited from the
            `EuroLeagueData` class. Choose one of:
            - 'E' for Euroleague
            - 'U' for Eurocup
            Defaults to "E".
    """

    def get_team_stats(
        self,
        endpoint: str,
        params: dict = {},
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame",
    ) -> pd.DataFrame:
        """
        A wrapper functions for collecting teams' stats.
        Allows for three types of data:
        - all seasons
        - single season
        - range of seasons

        Args:

            endpoint (str): The type of stats to fetch. Available values:
                - traditional
                - advanced
                - opponentsTraditional
                - opponentsAdvanced

            params (Dict[str, Union[str, int]]): A dictionary of the parmaters
                for the get request.

            phase_type_code (Optional[str], optional): The phase of the season,
                available variables:
                - "RS" (regular season)
                - "PO" (play-off)
                - "FF" (final four)
                Defaults to None, which includes all phases.

            statistic_mode (str, optional): The aggregation of statistics,
                available variables:
                - PerGame
                - Accumulated
                Defaults to "PerGame".

        Raises:

            ValueError: If the endpoint is not applicable

            ValueError: If the phase_type_code is not applicable

            ValueError: If the statistic_mode is not applicable

        Returns:

            pd.DataFrame: A dataframe with the teams' stats.
        """

        available_endpoints = [
            "traditional",
            "advanced",
            "opponentsTraditional",
            "opponentsAdvanced",
        ]
        available_phase_type_code = ["RS", "PO", "FF"]
        available_stat_mode = ["PerGame", "Accumulated"]

        raise_error(endpoint, "Statistic type", available_endpoints, False)
        raise_error(
            statistic_mode, "Statistic Aggregation", available_stat_mode, False
        )
        raise_error(
            phase_type_code, "Phase type code", available_phase_type_code, True
        )

        params["statisticMode"] = statistic_mode
        params["phaseTypeCode"] = phase_type_code
        params["limit"] = 400

        url_ = f"{self.url}/statistics/teams/{endpoint}"

        r = get_requests(url_, params=params)
        data = r.json()
        if data["total"] < len(data["teams"]):
            params["limit"] = len(data["teams"]) + 1
            r = get_requests(url_, params=params)
            data = r.json()
        df = pd.json_normalize(data["teams"])
        return df

    def get_team_stats_all_seasons(
        self,
        endpoint: str,
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame",
    ) -> pd.DataFrame:
        """
        A function that gets the team stats for all seasons

        Args:

            endpoint (str): The type of stats to fetch. Available values:
                - traditional
                - advanced
                - opponentsTraditional
                - opponentsAdvanced

            phase_type_code (Optional[str], optional): The phase of the season,
                available variables:
                - "RS" (regular season)
                - "PO" (play-off)
                - "FF" (final four)
                Defaults to None, which includes all phases.

            statistic_mode (str, optional): The aggregation of statistics,
                available variables:
                - PerGame
                - Accumulated
                Defaults to "PerGame".

        Returns:

            pd.DataFrame: A dataframe with the teams' stats
        """
        params = {"SeasonMode": "All"}
        df = self.get_team_stats(
            endpoint, params, phase_type_code, statistic_mode
        )
        return df

    def get_team_stats_single_season(
        self,
        endpoint: str,
        season: int,
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame",
    ) -> pd.DataFrame:
        """
        A function that returns the teams' stats in a single season

        Args:

            endpoint (str): The type of stats to fetch. Available values:
                - traditional
                - advanced
                - opponentsTraditional
                - opponentsAdvanced

            season (int): The start year of the season

            phase_type_code (Optional[str], optional): The phase of the season,
                available variables:
                - "RS" (regular season)
                - "PO" (play-off)
                - "FF" (final four)
                Defaults to None, which includes all phases.

            statistic_mode (str, optional): The aggregation of statistics,
                available variables:
                - PerGame
                - Accumulated
                Defaults to "PerGame".

        Returns:

            pd.DataFrame: A dataframe with the teams' stats
        """
        params = {
            "SeasonMode": "Single",
            "SeasonCode": f"{self.competition}{season}",
        }
        df = self.get_team_stats(
            endpoint, params, phase_type_code, statistic_mode
        )
        return df

    def get_team_stats_range_seasons(
        self,
        endpoint: str,
        start_season: int,
        end_season: int,
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame",
    ) -> pd.DataFrame:
        """
        A function that returns the teams' stats in a range of seasons

        Args:

            endpoint (str): The type of stats to fetch. Available values:
                - traditional
                - advanced
                - opponentsTraditional
                - opponentsAdvanced

            start_season (int): The start year of the start season

            end_season (int): The end year of the end season

            phase_type_code (Optional[str], optional): The phase of the season,
                available variables:
                - "RS" (regular season)
                - "PO" (play-off)
                - "FF" (final four)
                Defaults to None, which includes all phases.

            statistic_mode (str, optional): The aggregation of statistics,
                available variables:
                - PerGame
                - Accumulated
                Defaults to "PerGame".

        Returns:

            pd.DataFrame: A dataframe with the teams' stats
        """
        params = {
            "SeasonMode": "Range",
            "FromSeasonCode": f"{self.competition}{start_season}",
            "ToSeasonCode": f"{self.competition}{end_season}",
        }
        df = self.get_team_stats(
            endpoint, params, phase_type_code, statistic_mode
        )
        return df

    def get_team_advanced_stats_single_game(self, season: int, gamecode: int):
        """
        In this function we derive team advanced stats from a single game
        that are not provided by the API but can be easily calculated from
        play-by-play that are given from the API, i.e.
            - Number of Possessions
            - Pace

        Args:
            season (int): The start year of the season
            gamecode (int): The game-code of the game of interest.
                It can be found on Euroleague's website.
        """

        def convert_to_seconds(time_str):
            try:
                minutes, seconds = map(int, time_str.split(":"))
                return minutes * 60 + seconds
            except:
                return None

        def get_possession_number(df: pd.DataFrame, home_team_code: str):
            df["TotalSeconds"] = df["MARKERTIME"].apply(convert_to_seconds)
            filtered_mask = (df["PERIOD"].isin([1, 2, 3])) & (
                df["TotalSeconds"] <= 4
            )
            df_filtered = df[~filtered_mask].copy()

            codeteam = df_filtered["CODETEAM"].values
            playtype = df_filtered["PLAYTYPE"].values

            possessions = {"home": 0, "away": 0}
            last_possession_owner = None
            self_possession_end_conditions = {"2FGM", "3FGM", "TO", "FTM"}

            for i in range(len(codeteam)):
                current_team = codeteam[i]
                pt = playtype[i]

                current_owner = (
                    "home" if current_team == home_team_code else "away"
                )

                if pt in self_possession_end_conditions:
                    if last_possession_owner != current_owner:
                        possessions[current_owner] += 1
                        last_possession_owner = current_owner

                elif pt == "D":
                    new_owner = "away" if current_owner == "home" else "home"
                    if last_possession_owner != new_owner:
                        possessions[new_owner] += 1
                        last_possession_owner = new_owner

            return possessions

        boxscoredata = BoxScoreData(competition=self.competition)
        game_bxscr_stats = boxscoredata.get_player_boxscore_stats_data(
            season=season, gamecode=gamecode
        )
        totals_df = (
            game_bxscr_stats[game_bxscr_stats["Player_ID"] == "Total"]
            .set_index("Team")
            .T
        )
        minutes_played = int(totals_df.loc["Minutes"].iloc[0].split(":")[0])

        pbp = PlayByPlay(competition=self.competition)
        pbp_df = pbp.get_game_play_by_play_data(season, gamecode)

        home_team_code = totals_df.columns[1]

        possessions = get_possession_number(pbp_df, home_team_code)
        home_poss = possessions["home"]
        away_poss = possessions["away"]
        total_possessions = home_poss + away_poss

        pace = (
            (total_possessions / minutes_played * 5 * 40)
            if minutes_played > 0
            else 0
        )

        df_result = pd.DataFrame(
            {
                "Season": [season, season, season],
                "Gamecode": [gamecode, gamecode, gamecode],
                "Home": [1, 0, np.nan],
                "Possessions": [home_poss, away_poss, total_possessions],
                # TODO: Add Team's Pace
                "Pace": [np.nan, np.nan, pace],
            },
            index=[totals_df.columns[0], totals_df.columns[1], "Game"],
        )

        return df_result[["Season", "Gamecode", "Home", "Possessions", "Pace"]]
