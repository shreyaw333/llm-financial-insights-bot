import requests
import os
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# List of stocks we want to display
STOCKS = ["AAPL", "MSFT", "GOOGL", "NVDA", "AMZN", "TSLA"]

# Company names for display
COMPANY_NAMES = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation", 
    "GOOGL": "Alphabet Inc.",
    "NVDA": "NVIDIA Corporation",
    "AMZN": "Amazon.com Inc.",
    "TSLA": "Tesla Inc."
}

def get_stock_quote(symbol: str) -> Dict:
    """Get current stock quote for a single symbol"""
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "Global Quote" in data:
            quote = data["Global Quote"]
            
            # Extract the data we need
            current_price = float(quote["05. price"])
            change = float(quote["09. change"])
            change_percent = quote["10. change percent"].replace("%", "")
            
            return {
                "symbol": symbol,
                "company": COMPANY_NAMES.get(symbol, symbol),
                "price": round(current_price, 2),
                "change": round(change, 2),
                "change_percent": change_percent,
                "status": "success"
            }
        else:
            return {
                "symbol": symbol,
                "company": COMPANY_NAMES.get(symbol, symbol),
                "price": 0.0,
                "change": 0.0,
                "change_percent": "0.00",
                "status": "error"
            }
            
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return {
            "symbol": symbol,
            "company": COMPANY_NAMES.get(symbol, symbol),
            "price": 0.0,
            "change": 0.0,
            "change_percent": "0.00",
            "status": "error"
        }

def get_all_stocks() -> List[Dict]:
    """Get quotes for all stocks in our watchlist"""
    stocks_data = []
    
    for symbol in STOCKS:
        stock_data = get_stock_quote(symbol)
        stocks_data.append(stock_data)
    
    return stocks_data

# Mock data for testing (when API limits hit)
def get_mock_stocks() -> List[Dict]:
    """Return mock stock data for testing"""
    return [
        {"symbol": "AAPL", "company": "Apple Inc.", "price": 178.42, "change": 2.15, "change_percent": "1.22", "status": "success"},
        {"symbol": "MSFT", "company": "Microsoft Corporation", "price": 384.91, "change": 5.67, "change_percent": "1.49", "status": "success"},
        {"symbol": "GOOGL", "company": "Alphabet Inc.", "price": 141.25, "change": -1.83, "change_percent": "-1.28", "status": "success"},
        {"symbol": "NVDA", "company": "NVIDIA Corporation", "price": 441.78, "change": 12.34, "change_percent": "2.87", "status": "success"},
        {"symbol": "AMZN", "company": "Amazon.com Inc.", "price": 145.23, "change": 0.89, "change_percent": "0.62", "status": "success"},
        {"symbol": "TSLA", "company": "Tesla Inc.", "price": 238.45, "change": -4.21, "change_percent": "-1.74", "status": "success"}
    ]