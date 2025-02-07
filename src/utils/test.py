import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
'''
from solders.keypair import Keypair
from src.config import Config

try:
    keypair = Keypair.from_base58_string(Config.PRIVATE_KEY)
    print("✅ Valid Base58 Keypair:", keypair.pubkey())
except Exception as e:
    print("❌ Base58 Error:", e)
    try:
        keypair = Keypair.from_bytes(bytes.fromhex(Config.PRIVATE_KEY))
        print("✅ Valid Hex Keypair:", keypair.pubkey())
    except Exception as e:
        print("❌ Hex Error:", e)
        
        '''
        
import requests
from src.config import Config

def test_birdeye_api():
    url = "https://public-api.birdeye.so/defi/new_pairs"
    headers = {"X-API-KEY": Config.BIRDEYE_API_KEY}
    response = requests.get(url, headers=headers)
    print("Birdeye API Status Code:", response.status_code)
    try:
        data = response.json()
        print("Birdeye API Response JSON:", data)
    except Exception as e:
        print("Error decoding JSON response:", e)

if __name__ == "__main__":
    test_birdeye_api()

from solana.rpc.api import Client
from src.config import Config
from solders.keypair import Keypair

def test_helius_rpc():
    # Initialize your wallet from your Base58 keypair.
    wallet = Keypair.from_base58_string(Config.PRIVATE_KEY)
    client = Client(Config.RPC_URL)
    
    # Test by fetching the account balance
    balance_response = client.get_balance(wallet.pubkey())
    print("Helius RPC Balance Response:", balance_response)
    
    # Optionally, test another endpoint like getting the recent blockhash
    blockhash_response = client.get_recent_blockhash()
    print("Helius RPC Blockhash Response:", blockhash_response)

if __name__ == "__main__":
    test_helius_rpc()
