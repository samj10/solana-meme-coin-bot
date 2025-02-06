import os
from datetime import datetime
from solana.rpc.api import Client
from solana.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solders.keypair import Keypair
from config import Config

class SafeTrader:
    def execute_buy(self, contract, amount, price, mcap):
        """Paper trade buy with full details"""
        if self.paper_mode:
            print(f"\n📈 [PAPER] Buying {amount} SOL of {contract}")
            print(f"  Price: {price} | MCap: ${mcap:,.2f}")
            return True
      
        
    def execute_buy(self, token_address, amount):
        if self.paper_mode:
            print(f"\n📈 [PAPER] Buying {amount} SOL worth of {token_address[:6]}...")
            self.paper_balance -= amount
            self.paper_portfolio[token_address] = {
                'amount': amount,
                'entry_price': DataFetcher.get_token_price(token_address),
                'timestamp': datetime.now().isoformat()
            }
            return True
        else:
            # Real trading logic remains unchanged
            pass

    def get_balance(self):
        return self.paper_balance if self.paper_mode else (
            self.client.get_balance(self.wallet.public_key).value / 1e9
        )