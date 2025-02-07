import csv
import os
from datetime import datetime
from typing import List

class TradeLogger:
    def __init__(self):
        self.filename = f"trades_{datetime.now().strftime('%Y%m%d')}.csv"
        self.fieldnames = [
            'timestamp', 'contract', 'action', 'amount_sol',
            'entry_price', 'exit_price', 'entry_mcap', 'exit_mcap',
            'profit_loss', 'duration_min'
        ]
        self._initialize_logfile()
        
    def _initialize_logfile(self):
        """Create file with header if doesn't exist"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
                
    def log_trade(self, trade_data: dict):
        """Log trade with type checking"""
        with open(self.filename, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(trade_data)
            
    def get_performance(self) -> float:
        """Calculate cumulative performance from log"""
        try:
            with open(self.filename, 'r') as f:
                reader = csv.DictReader(f)
                return sum(float(row['profit_loss']) for row in reader)
        except FileNotFoundError:
            return 0.0