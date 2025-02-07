import os
import time
from datetime import datetime
from typing import Dict, Any

from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from src.config import Config
from .data_fetcher import DataFetcher

class SafeTrader:
    def __init__(self):
        self.paper_mode = os.getenv("PAPER_TRADING", "false").lower() == "true"
        
        print("ACTUAL PRIVATE KEY BEING USED:", repr(Config.PRIVATE_KEY))
        
        # Live trading mode: require a valid PRIVATE_KEY
        if not self.paper_mode:
            if not Config.PRIVATE_KEY:
                raise RuntimeError("PRIVATE_KEY environment variable required for live trading")
            try:
                # Use Base58 decoding since our key is a Base58-encoded full keypair
                self.wallet = Keypair.from_base58_string(Config.PRIVATE_KEY)
            except Exception as e:
                raise ValueError("Invalid PRIVATE_KEY format") from e
            self.pubkey = self.wallet.pubkey()
            self.client = Client(Config.RPC_URL)
        else:
            # Paper trading initialization
            self.paper_balance = 10.0
            self.paper_portfolio = {}
            self.active_trades = {}
            # Optionally, if you need a dummy wallet for paper mode, you can generate one:
            # self.wallet = Keypair()
            # self.pubkey = self.wallet.pubkey()
    
    def execute_buy(self, token_address: str, amount: float) -> bool:
        """Execute buy with risk checks"""
        if token_address in self.active_trades:
            return False
            
        if self.paper_mode:
            print(f"\n📈 [PAPER] Buying {amount} SOL of {token_address[:6]}")
            self.paper_balance -= amount
            self.active_trades[token_address] = {
                'amount': amount,
                'entry_time': datetime.now(),
                'entry_price': DataFetcher.get_token_metrics(token_address)['price']
            }
            return True
        else:
            # Real trading implementation goes here
            pass
    
    def execute_sell(self, token_address: str) -> float:
        """Execute sell order with validation"""
        if token_address not in self.active_trades:
            return 0.0
            
        trade = self.active_trades.pop(token_address)
        if self.paper_mode:
            current_price = DataFetcher.get_token_metrics(token_address)['price']
            profit_pct = ((current_price / trade['entry_price']) - 1) * 100
            self.paper_balance += trade['amount'] * (1 + profit_pct / 100)
            return profit_pct
        else:
            # Real trading implementation goes here
            pass
    
    def get_balance(self) -> float:
        """Get current available balance"""
        if self.paper_mode:
            return self.paper_balance + sum(
                trade['amount'] for trade in self.active_trades.values()
            )
        return self.client.get_balance(self.wallet.pubkey()).value / 1e9
