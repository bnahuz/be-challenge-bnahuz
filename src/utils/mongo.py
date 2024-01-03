from pymongo import MongoClient

class MongoDBConnection:
    def __init__(self, host='mongo-dev', port=27017, db_name:str='football'):
        """
        Initializes a MongoDBConnection object.

        Args:
            host (str): The hostname or IP address of the MongoDB server. Default is 'mongo-dev'.
            port (int): The port number of the MongoDB server. Default is 27017.
            db_name (str): The name of the database to connect to. Default is 'football'.
        """
        self.host = host
        self.port = port
        self.client = MongoClient(f'mongodb://admin:pass@{host}:{port}/')
        self.db = self.client[db_name]

    def insert_document(self, collection_name, document):
        """
        Inserts a single document into the specified collection.

        Args:
            collection_name (str): The name of the collection to insert the document into.
            document (dict): The document to be inserted.

        Returns:
            str: The ID of the inserted document.
        """
        if self.db is None:
            raise ValueError("Database not connected.")

        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return result.inserted_id

    def insert_many_documents(self, collection_name, documents):
        """
        Inserts multiple documents into the specified collection.

        Args:
            collection_name (str): The name of the collection to insert the documents into.
            documents (list): A list of documents to be inserted.

        Returns:
            list: The IDs of the inserted documents.
        """
        if self.db is None:
            raise ValueError("Database not connected.")

        collection = self.db[collection_name]
        result = collection.insert_many(documents)
        return result.inserted_ids

    def upsert_document(self, collection_name, query, update):
        """
        Upserts a document into the specified collection.

        Args:
            collection_name (str): The name of the collection to upsert the document into.
            query (dict): The query to find the document.
            update (dict): The update to be applied to the document.

        Returns:
            int: The number of modified documents.
        """
        if self.db is None:
            raise ValueError("Database not connected.")

        collection = self.db[collection_name]
        result = collection.update_one(query, {'$set': update}, upsert=True)
        return result.modified_count

    def update_many_documents(self, collection_name, query, update):
        """
        Updates multiple documents in the specified collection.

        Args:
            collection_name (str): The name of the collection to update the documents in.
            query (dict): The query to find the documents.
            update (dict): The update to be applied to the documents.

        Returns:
            int: The number of modified documents.
        """
        if self.db is None:
            raise ValueError("Database not connected.")

        collection = self.db[collection_name]
        result = collection.update_many(query, {'$set': update})
        return result.modified_count

    def find_document(self, collection_name, query):
        """
        Finds a document in the specified collection.

        Args:
            collection_name (str): The name of the collection to find the document in.
            query (dict): The query to find the document.

        Returns:
            dict: The found document.
        """
        if self.db is None:
            raise ValueError("Database not connected.")

        collection = self.db[collection_name]
        return collection.find_one(query)
    
    def get_all_documents(self, collection_name):
        """
        Retrieves all documents from the specified collection.

        Args:
            collection_name (str): The name of the collection to retrieve the documents from.

        Returns:
            list: A list of all documents in the collection.
        """
        if self.db is None:
            raise ValueError("Database not connected.")

        collection = self.db[collection_name]
        data = collection.find()
        return list(data)

    def check_team(self, teamId: int):
        """
        Checks if a team exists in the 'teams' collection.

        Args:
            teamId (int): The ID of the team to check.

        Returns:
            dict or bool: The team document if it exists, False otherwise.
        """
        if self.db is None:
            raise ValueError("Database not connected.")
        
        collection = self.db['teams']
        team = collection.find_one({'id': teamId})
        if team:
            return team
        else:
            return False

    def update_team(self, teamId: int, leagueId: int) -> int:
        """
        Updates the league ID of a team in the 'teams' collection.

        Args:
            teamId (int): The ID of the team to update.
            leagueId (int): The new league ID.

        Returns:
            int: The number of modified teams.
        """
        if self.db is None:
            raise ValueError("Database not connected.")
        collection = self.db['teams']
        team = collection.update_one({'id': teamId}, {'$push': {'leaugeId': leagueId}})
        return team.modified_count

    def close_connection(self):
        """
        Closes the connection to the MongoDB server.
        """
        self.client.close()