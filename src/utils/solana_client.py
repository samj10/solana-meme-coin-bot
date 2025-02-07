from solana.rpc.api import Client
from solana.transaction import Transaction
from solders.keypair import Keypair
from config import Config
import requests

class SolanaHandler:
    def __init__(self):
        self.client = Client(Config.RPC_URL)
        if Config.PRIVATE_KEY:
            self.wallet =  Keypair.from_base58_string(Config.PRIVATE_KEY)
        else:
            self.wallet = None  # Paper trading mode
            
    def validate_transaction(self, instruction):
        """Simulate transaction before sending"""
        try:
            return self.client.simulate_transaction(Transaction().add(instruction))
        except (requests.exceptions.RequestException, Exception) as e:
            print(f"Transaction validation failed: {str(e)}")
            return None