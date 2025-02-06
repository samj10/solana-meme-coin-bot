import requests
import numpy as np
from config import Config

class DeepSeekLearner:
    def __init__(self):
        self.last_analysis = "No recommendations yet"
        self.trade_history = []

    def analyze_trade(self, trade_data):
        try:
            response = requests.post(
                Config.DEEPSEEK_LEARN_URL,
                headers={"Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}"},
                json={"trade": trade_data}
            )
            self.last_analysis = response.json().get('analysis', 'No response')
            self.trade_history.append(trade_data)
        except Exception as e:
            print(f"DeepSeek error: {str(e)}")

    def get_latest_advice(self):
        return self.last_analysis

    def get_strategy_params(self):
        return {
            'buy_amount': Config.INITIAL_BUY_AMOUNT,
            'profit_target': 1.25,
            'stop_loss': 0.85
        }