import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Network
    RPC_URL = os.getenv("RPC_URL")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    
    # APIs
    BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    
    # Trading Parameters
    INITIAL_BUY_AMOUNT = 0.01  # SOL
    MAX_POSITION_SIZE = 0.1    # SOL
    LEARNING_RATE = 0.01
    SAFETY_MAX_SOL = float(os.getenv("SAFETY_MAX_SOL", 0.5))
    
    # DeepSeek Endpoints
    DEEPSEEK_LEARN_URL = "https://api.deepseek.com/v1/learn"