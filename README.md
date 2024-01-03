# BE Santex Technical Challenge

## Introduction
This GitHub repository contains the result of a Python technical challenge for Santex Group. The proposed challenge aimed to test skills and knowledge in the Python programming language, covering various fundamental aspects and concepts.

## Challenge Objective
The objective of this technical challenge was to expose an API from https://www.football-data.org/

## Technologies Used

The technical challenge was solved using the following technologies, libraries, and tools in Python:

* Python 3.10
* Flask Framework
* MongoDB
* MongoDB Express Framework
* Requests Library
* Pymongo Library

## Requirements

* Docker
* Docker Compose
* API Client(Postman, Insominia, Paw)


## Usage Instructions

To run the project, follow these steps:

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/bnahuz/be-challenge-bnahuz.git
    ```

2. Navigate to the project directory:

    ```bash
    cd be-challenge-bnahuz
    ```

3. Start the project servers:

    ```bash
    docker compose up
    ```
    This will start the project and all the dependencies.

4. Access the project:
    
    Open your API Client and make requests to `http://127.0.0.1:5000` to use the API.

    Aditionaly, you can check database using mongo express accessing `http://127.0.0.1:8081`

5. Available routes can be found on ROUTES.MD