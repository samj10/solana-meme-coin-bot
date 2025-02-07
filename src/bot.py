from solders.keypair import Keypair
import sys
import time
from datetime import datetime
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import Dict, Any

#absolute imports
from utils.data_fetcher import DataFetcher
from utils.trading import SafeTrader  
from utils.logging_util import TradeLogger
from config import Config

class TradingBot:
    def __init__(self):
        self.trader = SafeTrader()
        self.logger = TradeLogger()
        self.active_trades = {}
        self.start_time = datetime.now()
        
    def _process_pair(self, pair: Dict):
        """Handle new token pair with safety checks"""
        if pair['address'] in self.active_trades:
            return
            
        if len(self.active_trades) >= Config.MAX_CONCURRENT_TRADES:
            return
            
        if self.trader.get_balance() < Config.INITIAL_BUY_AMOUNT:
            return
            
        success = self.trader.execute_buy(
            pair['address'],
            Config.INITIAL_BUY_AMOUNT
        )
        
        if success:
            self.active_trades[pair['address']] = {
                'entry_time': datetime.now(),
                'entry_price': pair['price'],
                'entry_mcap': pair['mcap']
            }

    def _monitor_open_trades(self):
        """Check sell conditions with proper duration calculation"""
        for address in list(self.active_trades.keys()):
            metrics = DataFetcher.get_token_metrics(address)
            if not metrics:
                continue
                
            trade = self.active_trades[address]
            duration = (datetime.now() - trade['entry_time']).total_seconds() / 60
            current_price = metrics['price']
            
            profit_pct = ((current_price / trade['entry_price']) - 1) * 100
            if profit_pct >= Config.PROFIT_TARGET or profit_pct <= -Config.STOP_LOSS:
                self.logger.log_trade({
                    'timestamp': datetime.now().isoformat(),
                    'contract': address,
                    'action': 'SELL',
                    'amount_sol': Config.INITIAL_BUY_AMOUNT,
                    'entry_price': trade['entry_price'],
                    'exit_price': current_price,
                    'entry_mcap': trade['entry_mcap'],
                    'exit_mcap': metrics['mcap'],
                    'profit_loss': profit_pct,
                    'duration_min': round(duration, 2)
                })
                self.trader.execute_sell(address)
                del self.active_trades[address]

    def run(self):
        print("\n🚀 Starting Trading Bot")
        print(f"Mode: {'PAPER' if self.trader.paper_mode else 'LIVE'}")
        print("-----------------------------")
        
        try:
            while True:
                new_pairs = DataFetcher.get_new_pairs()
                for pair in new_pairs:
                    self._process_pair(pair)
                
                self._monitor_open_trades()
                time.sleep(10)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Bot stopped by user")
            print(f"📊 Total Profit: {self.logger.get_performance():.2f}%")
            

if __name__ == "__main__":
    # Add project root to Python path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    bot = TradingBot()
    bot.run()