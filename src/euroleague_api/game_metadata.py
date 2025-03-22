import pandas as pd
from euroleague_api.utils import get_requests

class GameMetadata:
    def __init__(self, competition_code):
        self.competition_code = competition_code

    def get_game_metadata(self, season, gamecode):
        base_url = 'https://live.euroleague.net/api/Header?gamecode={}&seasoncode={}{}&disp='
        url = base_url.format(gamecode, self.competition_code, season)
        response = get_requests(url)
        if response is None:
            raise ValueError(f"Failed to retrieve data for gamecode {gamecode}, season {season}")

        json_content = response.json()
        metadata = {
            'Phase': json_content.get('Phase'),
            'Round': json_content.get('Round'),
            'Date': json_content.get('Date'),
            'Hour': json_content.get('Hour').strip(),
            'Stadium': json_content.get('Stadium'),
            'StadiumCapacity': json_content.get('StadiumCapacity'),
            'TeamA': json_content.get('TeamA'),
            'TeamB': json_content.get('TeamB'),
            'CodeTeamA': json_content.get('CodeTeamA'),
            'CodeTeamB': json_content.get('CodeTeamB'),
            'CoachA': json_content.get('CoachA'),
            'CoachB': json_content.get('CoachB'),
            'ScoreA': json_content.get('ScoreA'),
            'ScoreB': json_content.get('ScoreB'),
            'Referees': [json_content.get('Referee1'), json_content.get('Referee2'), json_content.get('Referee3')],
        }

        return pd.DataFrame([metadata])
    
    def get_game_metadata_single_season(self, season):
        """
        Retrieves game metadata for all games in a single season.

        Args:
            season (int): The start year of the season.

        Returns:
            pd.DataFrame: A dataframe containing metadata for all games in the given season.
        """
        # Fetch the game codes for the given season
        game_codes = self.get_season_game_codes(season)

        # Collect metadata for all games
        all_metadata = []
        for gamecode in game_codes:
            try:
                metadata_df = self.get_game_metadata(season, gamecode)
                all_metadata.append(metadata_df)
            except Exception as e:
                print(f"Error retrieving metadata for game {gamecode}: {e}")

        # Concatenate all data into a single DataFrame
        if all_metadata:
            return pd.concat(all_metadata, ignore_index=True)
        else:
            return pd.DataFrame()  # Return empty DataFrame if no data was retrieved
        
    def get_season_game_codes(self, season: int) -> list:
        """
        Retrieves all game codes for a given season.

        Args:
            season (int): The start year of the season.

        Returns:
            list: A list of game codes for the given season.
        """
        game_metadata_df = self.get_game_metadata_season(season)
        return game_metadata_df["gamenumber"].tolist()
