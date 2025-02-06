import csv
from datetime import datetime

class TradeLogger:
    def __init__(self):
        self.filename = f"trades_{datetime.now().strftime('%Y%m%d')}.csv"
        self.header = [
            'timestamp', 'contract', 'action', 'amount_sol',
            'entry_price', 'exit_price', 'entry_mcap', 'exit_mcap',
            'profit_loss', 'duration_min'
        ]
        self._init_file()

    def _init_file(self):
        with open(self.filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.header)

    def log_trade(self, trade_data):
        """Log to CSV and terminal with full details"""
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([trade_data[k] for k in self.header])
        
        # Terminal output
        action = trade_data['action']
        contract = trade_data['contract']
        amount = trade_data['amount_sol']
        
        if action == 'BUY':
            print(f"\n🟢 BOUGHT {amount} SOL of {contract}")
            print(f"  Entry Price: {trade_data['entry_price']}")
            print(f"  Market Cap: ${trade_data['entry_mcap']:,.2f}")
        elif action == 'SELL':
            profit = trade_data['profit_loss']
            color = "\033[92m" if profit > 0 else "\033[91m"
            print(f"\n{color}🔴 SOLD {amount} SOL of {contract}")
            print(f"  Exit Price: {trade_data['exit_price']}")
            print(f"  Exit Market Cap: ${trade_data['exit_mcap']:,.2f}")
            print(f"  Profit: {profit:.2f}% ({trade_data['duration_min']} mins)\033[0m")