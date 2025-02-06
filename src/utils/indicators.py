import pandas as pd

class TradingSignals:
    @staticmethod
    def detect_pump(data):
        """Identify 5-minute volume spikes :cite[6]"""
        df = pd.DataFrame(data)
        df['volume_ma'] = df['volume'].rolling(3).mean()
        return df['volume'].iloc[-1] > 2 * df['volume_ma'].iloc[-2]
    
    @staticmethod
    def rsi_signal(prices):
        """RSI-based mean reversion :cite[3]"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs.iloc[-1]))