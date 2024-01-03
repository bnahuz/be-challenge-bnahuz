import requests
from time import sleep

class FootballAPIConsumer:
    """
    A class that represents a consumer for a football API.

    Attributes:
        api_key (str): The API key used for authentication.

    Methods:
        request(url: str, n_tries=5) -> list: Sends a GET request to the specified URL with the provided headers and returns the response as a JSON object.
    """

    def __init__(self):
        self.api_key = "0a0501c7be5f4433acbc8000c8376476" #os.environ['FOOTBALL_TOKEN']

    def request(self, url: str, n_tries=5) -> list:
        """
        Sends a GET request to the specified URL with the provided headers and returns the response as a JSON object.

        Args:
            url (str): The URL to send the request to.
            n_tries (int): The number of times to retry the request in case of certain status codes. Defaults to 5.

        Returns:
            list: The response as a JSON object.

        Raises:
            Exception: If the response status code is not 200, 429, or 500.
        """
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.api_key
        }
        
        print(f'[INFO] - Getting data from {url} with params')
        response = requests.get(url, headers=headers)
        for tries in range(n_tries):
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print(f"[WARNING] - Status Code 429: Too Many requests, try number {tries + 1}, trying again.")
                sleep(60)
                continue
            elif response.status_code == 500:
                print(f"[WARNING] - Status Code 500: Internal Error, try number {tries + 1}, trying again.")
                sleep(10)
                continue
            else:
                raise Exception(f"[ERROR] - Status code {response.status_code}")