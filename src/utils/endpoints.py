from .consumer import FootballAPIConsumer
from .mongo import MongoDBConnection

consumer = FootballAPIConsumer()

def get_league(competition_code: str, import_seasons : bool = False) -> dict:
    """
    Get league information for a given competition code.

    Args:
        competition_code (str): The code of the competition.
        import_seasons (bool, optional): Whether to import seasons data. Defaults to False.

    Returns:
        dict: A dictionary containing the league information.
    """
    url = f'http://api.football-data.org/v4/competitions/{competition_code}'
   
    data = consumer.request(url)
    try:
        if data.get('seasons'):
            data.pop('seasons')
        return {
            'status': 200,
            'competition': data.get('name'),
            'leagueId': data.get('id'),
            'message': 'Data found',
            'data': data   
        }
    except:
        return {
            'status': 404,
            'message': 'No data found'
        }

def get_teams(competition_code: str, competition_id:int,  with_squad:bool = True, season:str = None) -> dict:
    """
    Get teams information for a given competition code.

    Args:
        competition_code (str): The code of the competition.
        competition_id (int): The ID of the competition.
        with_squad (bool, optional): Whether to include squad information. Defaults to True.
        season (str, optional): The season to filter the teams. Defaults to None.

    Returns:
        dict: A dictionary containing the teams information.
    """
    url = f'http://api.football-data.org/v4/competitions/{competition_code}/teams'
    if season:
        url += f'?season={season}'
    data = consumer.request(url).get('teams')
    teams_data = []
    persons_data = []
    db = MongoDBConnection(db_name='football')
    for team in data:
        teamId = team.get('id')
        check = db.check_team(teamId)
        if check:
            print(f'[INFO] - Team {teamId} already exists in MongoDB')
            db.update_team(teamId, competition_id)
            continue
        else:
            team_data = {
                'id': team.get('id'),
                'leaugeId': [competition_id],
                'name': team.get('name').replace(' ', '_').lower(),
                'tla': team.get('tla'),
                'shortName': team.get('shortName'),
                'areaId': team.get('area').get('id'),
                'areaName': team.get('area').get('name'),
                'address': team.get('address')
            }
            teams_data.append(team_data)
            if with_squad:
                if not team.get('squad'):
                    coach = team.get('coach')
                    coach['teamId'] = team.get('id')
                    coach['position'] = 'Coach'
                    del coach['firstName']
                    del coach['lastName']
                    del coach['contract']
                    persons_data.append(coach)
                else:
                    for player in team['squad']:
                        player['teamId'] = team.get('id')
                        persons_data.append(player)
    return {
            'teams_data': teams_data,
            'persons_data': persons_data,
            'data': data
        }
