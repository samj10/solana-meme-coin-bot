import requests
from config import Config

class DataFetcher:
    @staticmethod
    def get_new_pairs():
        """Fetch new pairs with market cap data"""
        url = "https://public-api.birdeye.so/defi/new_pairs"
        headers = {"X-API-KEY": Config.BIRDEYE_API_KEY}
        try:
            response = requests.get(url, headers=headers)
            return [
                {
                    'address': p['address'],
                    'symbol': p['symbol'],
                    'price': p['price'],
                    'liquidity': p['liquidity'],
                    'mcap': p['fdv'],
                    'age': p['age_minutes']
                } for p in response.json().get('data', [])
                if p['liquidity'] > 5000
            ]
        except Exception as e:
            print(f"Data error: {str(e)}")
            return []

    @staticmethod
    def get_token_metrics(address):
        """Get current market cap"""
        url = f"https://public-api.birdeye.so/defi/token_metrics?address={address}"
        headers = {"X-API-KEY": Config.BIRDEYE_API_KEY}
        try:
            res = requests.get(url, headers=headers)
            data = res.json()
            return {
                'price': data.get('price', 0),
                'mcap': data.get('fdv', 0)
            }
        except:
            return {'price': 0, 'mcap': 0}