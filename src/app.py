from flask import Flask, jsonify, request
from utils.mongo import MongoDBConnection
from utils.main import process_data

app = Flask(__name__)

client = MongoDBConnection(db_name='football')
db = client.db
leagues = db['leagues']  
players = db['people']
teams = db['teams']

@app.route('/import_league', methods=['POST'])
def import_league_endpoint():
    """
    Import a league by processing the data based on the provided league code.

    Returns:
        JSON response: Processed data of the league.
    """
    request_data = request.json
    league_code = request_data.get('league_code')

    if not league_code:
        return jsonify({'message': 'League code are required!'}), 400

    try:
        processed_data = process_data(league_code)
        return jsonify(processed_data)
    except Exception as e:
        return jsonify({'message': f'Error processing data: {str(e)}'}), 500

@app.route('/leagues', methods=['GET'])
def get_leagues():
    """
    Get all the leagues.

    Returns:
        JSON response: List of leagues.
    """
    data = list(leagues.find())
    for item in data:
        item['_id'] = str(item['_id'])
    return jsonify(data)

@app.route('/league/<string:league_code>/players', methods=['GET'])
def get_players_by_league(league_code):
    """
    Get players by league.

    Args:
        league_code (str): The code of the league.

    Returns:
        JSON response: List of players in the league.
    """
    league = leagues.find_one({'code': league_code})
    
    if league:
        team_filter = request.args.get('team_name')
        query = {'leaugeId': league['id']}
        if team_filter:
            team_data = teams.find_one({'name': team_filter})
            if team_data:
                query['id'] = team_data['id']
            else:
                return jsonify({'message': 'Team not found'}), 404

        teams_data = teams.find(query)
        team_ids = [team['id'] for team in teams_data]
        
        players_data = players.find({'teamId': {'$in': team_ids}})
        players_list = list(players_data)
        for item in players_list:
            item['_id'] = str(item['_id'])
        if players_list:
            return jsonify(players_list)
        else:
            return jsonify({'message': f'{team_filter} is not part of the {league_code} league'}), 404
    else:
        return jsonify({'message': 'League code not found'}), 404

@app.route('/players', methods=['GET'])
def get_players():
    """
    Retrieve all players from the database.

    Returns:
        A JSON response containing the list of players.
    """
    data = list(players.find())
    for item in data:
        item['_id'] = str(item['_id'])  
    return jsonify(data)

@app.route('/players/<string:team_name>', methods=['GET'])
def get_players_by_team_name(team_name):
    """
    Retrieves a list of players belonging to a specific team.

    Parameters:
    team_name (str): The name of the team.

    Returns:
    list: A list of players belonging to the team.

    Raises:
    404: If the team is not found.
    400: If an error occurs during the retrieval process.
    """
    try:
        team = teams.find_one({'name': team_name})

        if team:
            players_data = players.find({'teamId': team['id']})
            players_list = list(players_data)
            for item in players_list:
                item['_id'] = str(item['_id']) 
            return jsonify(players_list)
        else:
            return jsonify({'message': 'Team not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/coaches', methods=['GET'])
def get_coaches():
    """
    Get all the coaches.

    Returns:
        JSON response: List of coaches.
    """
    data = list(players.find({'position': 'Coach'}))
    if data:
        for item in data:
            item['_id'] = str(item['_id'])  
        return jsonify(data)
    else:
        return jsonify({'message': 'No coaches found'}), 404

@app.route('/teams', methods=['GET'])
def get_teams():
    """
    Get all the teams.

    Returns:
        JSON response: List of teams.
    """
    data = list(teams.find())
    for item in data:
        item['_id'] = str(item['_id'])  
    return jsonify(data)

@app.route('/team/<int:id>', methods=['GET'])
def get_team_by_id(id):
    """
    Get a team by ID.

    Args:
        id (int): The ID of the team.

    Returns:
        JSON response: The team details.
    """
    data = teams.find_one({'id': id})
    if data:
        data['_id'] = str(data['_id'])
        return jsonify(data)
    else:
        return jsonify({'message': 'Team not found'}), 404

@app.route('/team', methods=['GET'])
def get_team_by_name():
    """
    Get a team by name.

    Returns:
        JSON response: The team details.
    """
    team_name = request.args.get('name')
    if not team_name:
        return jsonify({'message': 'Team name not provided'}), 400
    
    team = teams.find_one({'name': team_name})
    
    if team:
        team['_id'] = str(team['_id'])
        resolve_players = request.args.get('resolve_players')
        if resolve_players and resolve_players.lower() == 'true':
            team_players = players.find({'teamId': team['id']})
            players_list = list(team_players)
            for player in players_list:
                player['_id'] = str(player['_id'])
            
            team['players'] = players_list
        
        return jsonify(team)
    else:
        return jsonify({'message': 'Team not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000)