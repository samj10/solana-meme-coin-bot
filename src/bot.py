import time
from datetime import datetime
from utils.data_fetcher import DataFetcher
from utils.trading import SafeTrader
from utils.logging_util import TradeLogger

class TradingBot:
    def __init__(self):
        self.trader = SafeTrader()
        self.logger = TradeLogger()
        self.active_trades = {}
        self.start_time = datetime.now()

    def _process_pair(self, pair):
        """Handle new token pair"""
        strategy = {
            'buy_amount': 0.01,
            'profit_target': 25,
            'stop_loss': 15
        }
        
        if pair['price'] < 0.0001:
            entry_mcap = pair['mcap']
            success = self.trader.execute_buy(
                pair['address'],
                strategy['buy_amount'],
                pair['price'],
                entry_mcap
            )
            
            if success:
                self.active_trades[pair['address']] = {
                    'entry_time': datetime.now(),
                    'entry_price': pair['price'],
                    'entry_mcap': entry_mcap,
                    'amount': strategy['buy_amount']
                }

    def _monitor_open_trades(self):
        """Check sell conditions"""
        for address in list(self.active_trades.keys()):
            metrics = DataFetcher.get_token_metrics(address)
            trade = self.active_trades[address]
            
            current_price = metrics['price']
            entry_price = trade['entry_price']
            profit_pct = ((current_price / entry_price) - 1) * 100
            
            if profit_pct >= 25 or profit_pct <= -15:
                exit_mcap = metrics['mcap']
                duration = (datetime.now() - trade['entry_time']).seconds // 60
                
                self.logger.log_trade({
                    'timestamp': datetime.now().isoformat(),
                    'contract': address,
                    'action': 'SELL',
                    'amount_sol': trade['amount'],
                    'entry_price': entry_price,
                    'exit_price': current_price,
                    'entry_mcap': trade['entry_mcap'],
                    'exit_mcap': exit_mcap,
                    'profit_loss': profit_pct,
                    'duration_min': duration
                })
                del self.active_trades[address]

    def run(self):
        print("\n🚀 Starting Paper Trading Bot")
        print("-----------------------------")
        print("Continuous mode - CTRL+C to exit\n")
        
        try:
            while True:
                print("🔍 Scanning new pairs...", end="\r")
                new_pairs = DataFetcher.get_new_pairs()
                
                for pair in new_pairs:
                    self._process_pair(pair)
                
                self._monitor_open_trades()
                time.sleep(10)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Bot stopped by user")
            print(f"💼 Final Balance: {self.trader.get_balance():.2f} SOL")
            print(f"📊 Total Profit: {self.logger.get_performance():.2f}%")

if __name__ == "__main__":
    bot = TradingBot()
    bot.run()