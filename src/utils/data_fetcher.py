import requests
import time
from typing import List, Dict, Any
from config import Config

class DataFetcher:
    @staticmethod
    def _api_request(url: str) -> Any:
        """Generic API request with retry logic"""
        headers = {"X-API-KEY": Config.BIRDEYE_API_KEY}
        for attempt in range(Config.API_RETRIES):
            try:
                response = requests.get(url, headers=headers, timeout=5)
                response.raise_for_status()
                return response.json().get('data', [])
            except Exception as e:
                if attempt < Config.API_RETRIES - 1:
                    time.sleep(Config.API_RETRY_DELAY)
                continue
        return []

    @staticmethod
    def get_new_pairs() -> List[Dict]:
        """Filter new pairs using configurable thresholds"""
        data = DataFetcher._api_request("https://public-api.birdeye.so/defi/new_pairs")
        return [
            p for p in data
            if p['liquidity'] > Config.LIQUIDITY_THRESHOLD
            and p['price'] < Config.PRICE_THRESHOLD
        ]
    
    @staticmethod
    def get_token_metrics(address: str) -> Dict[str, float]:
        """Get current token metrics with fallback"""
        data = DataFetcher._api_request(
            f"https://public-api.birdeye.so/defi/token_metrics?address={address}"
        )
        return {
            'price': data.get('price', 0.0),
            'mcap': data.get('fdv', 0.0)
        }