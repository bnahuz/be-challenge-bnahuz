from .endpoints import *
from .mongo import MongoDBConnection

def process_data(league_code):
    """
    Process data for a given league code.

    Args:
        league_code (str): The code of the league.

    Returns:
        dict: A dictionary containing the result of the data processing.
            If successful, the dictionary will have a 'message' key with a success message.
            If there is an error, the dictionary will have a 'message' key with an error message.
    """
    league = get_league(league_code)
    if league['status'] != 200:
        print(f'[ERROR] - League {league_code} not found')
        return False
    league_id = league['leagueId']
    league = league['data']

    teams = get_teams(league_code, league_id)
    for team in teams['data']:
        team['leagueId'] = league_id
    if not teams:
        print(f'[ERROR] - No teams found for league {league_code}')
        return False
    
    try:
        mongo = MongoDBConnection(db_name='football')

        mongo.insert_document('leagues', league)
        mongo.insert_many_documents('teams', teams['teams_data'])
        mongo.insert_many_documents('people', teams['persons_data'])

        mongo.close_connection()
        return {
            'message': f'League {league_code} data downloaded and saved in MongoDB'
        }
    except Exception as e:
        return {
            'message': f'Error processing data: {str(e)}'
        }