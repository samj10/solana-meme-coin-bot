import os
from pathlib import Path
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parent.parent  # Goes up 2 levels from src/config.py
env_path = project_root / ".env"

print(f"\n🔍 Looking for .env at: {env_path}")
print(f"Does .env exist? {env_path.exists()}\n")

# --------------------------------------------------
# 2. Load Environment
# --------------------------------------------------
load_dotenv(dotenv_path=env_path)

class Config:
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    RPC_URL = os.getenv("RPC_URL", "https://api.mainnet-beta.solana.com")
    BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY", "")
    
    # Trading Parameters
    INITIAL_BUY_AMOUNT: float = 0.01  # SOL
    MAX_POSITION_SIZE: float = 0.1     # SOL
    SAFETY_MAX_SOL: float = float(os.getenv("SAFETY_MAX_SOL", 0.5))
    
    # Risk Management
    LIQUIDITY_THRESHOLD: int = 5000      # Minimum liquidity in USD
    PRICE_THRESHOLD: float = 0.0001        # Maximum entry price
    PROFIT_TARGET: float = 25.0            # Percentage
    STOP_LOSS: float = 15.0                # Percentage
    MAX_CONCURRENT_TRADES: int = 5         # Simultaneous positions
    
    # API Settings
    API_RETRIES: int = 3
    API_RETRY_DELAY: float = 1.0           # Seconds

    
