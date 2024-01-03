### Import League Endpoint

- **Endpoint**: `/import_league`
- **Method**: `POST`
- **Description**: Import a league by processing the data based on the provided league code.
- **Request Body**:
    ```json
    {
        "league_code": "PD"
    }
    ```
- **Response**:
    - `200 OK`:
        ```json
        {
            "processed_data": { }
        }
        ```
    - `400 Bad Request`:
        ```json
        {
            "message": "League code is required!"
        }
        ```
    - `500 Internal Server Error`:
        ```json
        {
            "message": "Error processing data: <error_message>"
        }
        ```

### Get Leagues

- **Endpoint**: `/leagues`
- **Method**: `GET`
- **Description**: Get all the leagues.
- **Response**:
    ```json
    [
        {
            "_id": "123",
            "league_details": { }
        },
        {
            "_id": "456",
            "league_details": { }
        }
    ]
    ```

### Get Players by League

- **Endpoint**: `/league/<league_code>/players`
- **Method**: `GET`
- **Description**: Get players by league.
- **Parameters**:
    - `league_code`: The code of the league.
- **Query Parameters**:
    - `team_name`: Filter players by team name.
- **Response**:
    - `200 OK`:
        ```json
        [
            {
                "_id": "123",
                "player_details": { }
            },
            {
                "_id": "456",
                "player_details": { }
            }
        ]
        ```
    - `404 Not Found`:
        ```json
        {
            "message": "Team not found" 
        }
        ```
        ```json
        {
            "message": "<team_name> is not part of the <league_code> league"
        }
        ```
        ```json
        {
            "message": "League code not found"
        }
        ```

### Get Players

- **Endpoint**: `/players`
- **Method**: `GET`
- **Description**: Retrieve all players from the database.
- **Response**:
    ```json
    [
        {
            "_id": "123",
            "player_details": { }
        },
        {
            "_id": "456",
            "player_details": { }
        }
    ]
    ```

### Get Players by Team Name

- **Endpoint**: `/players/<team_name>`
- **Method**: `GET`
- **Description**: Retrieves a list of players belonging to a specific team.
- **Parameters**:
    - `team_name`: The name of the team.
- **Response**:
    - `200 OK`:
        ```json
        [
            {
                "id": "123",
                "player_details": { }
            },
            {
                "id": "456",
                "player_details": { }
            }
        ]
        ```
    - `404 Not Found`:
        ```json
        {
            "message": "Team not found"
        }
        ```
    - `400 Bad Request`:
        ```json
        {
            "message": "<error_message>"
        }
        ```

### Get Coaches

- **Endpoint**: `/coaches`
- **Method**: `GET`
- **Description**: Get all the coaches.
- **Response**:
    ```json
    [
        {
            "_id": "123",
            "coach_details": { }
        },
        {
            "_id": "456",
            "coach_details": { }
        }
    ]
    ```

### Get Teams

- **Endpoint**: `/teams`
- **Method**: `GET`
- **Description**: Get all the teams.
- **Response**:
    ```json
    [
        {
            "_id": "123",
            "team_details": { }
        },
        {
            "_id": "456",
            "team_details": { }
        }
    ]
    ```

### Get Team by ID

- **Endpoint**: `/team/<id>`
- **Method**: `GET`
- **Description**: Get a team by ID.
- **Parameters**:
    - `id`: The ID of the team.
- **Response**:
    - `200 OK`:
        ```json
        {
            "_id": "123",
            "team_details": { }
        }
        ```
    - `404 Not Found`:
        ```json
        {
            "message": "Team not found"
        }
        ```

### Get Team by Name

- **Endpoint**: `/team`
- **Method**: `GET`
- **Description**: Get a team by name.
- **Query Parameters**:
    - `name`: The name of the team.
    - `resolve_players`: Optional, if set to `true`, includes players' details.
- **Response**:
    - `200 OK`:
        ```json
        {
            "_id": "123",
            "team_details": { },
            "players": [
                {
                    "_id": "456",
                    "player_details": { }
                },
                {
                    "_id": "789",
                    "player_details": { }
                }
            ]
        }
        ```
    - `404 Not Found`:
        ```json
        {
            "message": "Team not found"
        }
        ```
    - `400 Bad Request`:
        ```json
        {
            "message": "Team name not provided"
        }
        ```