from solana.rpc.api import Client
from solana.transaction import Transaction
from solders.keypair import Keypair
from config import Config

class SolanaHandler:
    def __init__(self):
        self.client = Client(Config.RPC_URL)
        self.wallet = Keypair.from_secret_key(bytes.fromhex(Config.WALLET_PRIVATE_KEY))
    
    def send_transaction(self, instruction):
        """Execute trades with MEV protection :cite[9]"""
        transaction = Transaction().add(instruction)
        return self.client.send_transaction(transaction, self.wallet)