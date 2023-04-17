from tiingo import TiingoClient
from dotenv import load_dotenv
import os

class MyTiingoClient:
    """
    Configure Tiingo client with api key
    """
    load_dotenv()
    
    def __init__(self):
        self._tiingo_api_key = os.environ.get('TIINGO_APIKEY')
        self._config = self.get_client_config()
        self._client = self.get_client()

    def get_client_config(self):
        config = {}
        config['session'] = True
        config['api_key'] = self._tiingo_api_key
        return config

    def get_client(self):
        return TiingoClient(self._config)