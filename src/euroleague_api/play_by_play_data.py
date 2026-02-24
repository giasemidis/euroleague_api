import logging
from json.decoder import JSONDecodeError
import pandas as pd
import numpy as np
from .EuroLeagueData import EuroLeagueData
from .boxscore_data import BoxScoreData
from .utils import get_requests, get_pbp_lineups

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
        gamecode: int,
        include_ishometeam: bool = False,
    ) -> pd.DataFrame:
        """
        A function that gets the play-by-play data of a particular game.

        Args:

            season (int): The start year of the season

            gamecode (int): The game-code of the game of interest.
                It can be found on Euroleague's website.

            include_ishometeam (bool, optional): A bool indicator whether to
                include the `IsHomeTeam` column in the returned dataframe,
                which shows whether the action was performed by the home team
                or not. Defaults to False. Introduced for backward
                compatibility.

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
            logger.error(
                f"Game code, {gamecode}, season {season}, "
                "did not return valid JSON data."
            )
            raise exc

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

        if not all_data:
            logger.warning(
                f"No play-by-play data found for gamecode {gamecode} "
                f" and season {season}"
            )
            return pd.DataFrame()

        pbp_df = pd.concat(all_data).reset_index(drop=True)
        pbp_df["PLAYER"] = (
            pbp_df["PLAYER"].str.replace("  ", " ")
            .str.replace(" , ", ", ").str.strip()
        )
        pbp_df['CODETEAM'] = pbp_df['CODETEAM'].str.strip()
        pbp_df['PLAYER_ID'] = pbp_df['PLAYER_ID'].str.strip()
        pbp_df["PLAYTYPE"] = pbp_df["PLAYTYPE"].str.strip()
        pbp_df["MARKERTIME"] = pbp_df["MARKERTIME"].str.strip()
        if include_ishometeam:  # for backward compatibility
            home_team = data["CodeTeamA"]
            away_team = data["CodeTeamB"]
            pbp_df["IsHomeTeam"] = np.where(
                pbp_df["CODETEAM"] == home_team, True,
                np.where(pbp_df["CODETEAM"] == away_team,
                         False, None)  # type: ignore
            )
        pbp_df.insert(0, 'Season', season)
        pbp_df.insert(1, 'Gamecode', gamecode)
        # insert a TRUE_NUMBEROFPLAY column
        # often the NUMBEROFPLAY column is not in order
        pbp_df["TRUE_NUMBEROFPLAY"] = np.arange(pbp_df.shape[0])

        return pbp_df

    def get_game_play_by_play_data_round(
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

    def get_game_play_by_play_data_range_seasons(
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

    def get_game_pbp_data_lineups(
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

        # Fetch play-by-play data
        pbp_data = self.get_game_play_by_play_data(
            season=season, gamecode=gamecode, include_ishometeam=True)

        # Get the starting line-ups from boxscore data
        boxscoredata = BoxScoreData(competition=self.competition)
        try:
            game_bxscr_stats = boxscoredata.get_players_boxscore_stats(
                season=season, gamecode=gamecode)
        except Exception as e:  # noqa: E722
            logger.warning(
                f"Something went wrong when fetching boxscore data for "
                f"game {gamecode}, season {season}.\nError message: {e}. "
                "\nSkip and continue"
            )
            game_bxscr_stats = pd.DataFrame()

        pbp_df = get_pbp_lineups(
            pbp_df=pbp_data,
            boxscore_df=game_bxscr_stats,
            validate=validate
        )
        return pbp_df

    def get_game_pbp_data_lineups_round(
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
            season, round_number, self.get_game_pbp_data_lineups)
        return df

    def get_game_pbp_data_lineups_single_season(
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
            season, self.get_game_pbp_data_lineups)
        return data_df

    def get_game_pbp_data_lineups_range_seasons(
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
            start_season, end_season, self.get_game_pbp_data_lineups)
        return df
