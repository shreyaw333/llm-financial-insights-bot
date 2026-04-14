import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List

STOCKS = ["AAPL", "MSFT", "GOOGL", "NVDA", "AMZN", "TSLA"]

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
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.fast_info

        current_price = round(info.last_price, 2)
        prev_close = round(info.previous_close, 2)
        change = round(current_price - prev_close, 2)
        change_percent = round((change / prev_close) * 100, 4)

        return {
            "symbol": symbol,
            "company": COMPANY_NAMES.get(symbol, symbol),
            "price": current_price,
            "change": change,
            "change_percent": str(change_percent),
            "status": "success"
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
    """Fetch all stocks in parallel for speed"""
    results = {}

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(get_stock_quote, symbol): symbol for symbol in STOCKS}
        for future in as_completed(futures):
            symbol = futures[future]
            results[symbol] = future.result()

    # Return in original order
    return [results[symbol] for symbol in STOCKS]

def get_mock_stocks() -> List[Dict]:
    """Return mock stock data as fallback"""
    return [
        {"symbol": "AAPL", "company": "Apple Inc.", "price": 178.42, "change": 2.15, "change_percent": "1.22", "status": "success"},
        {"symbol": "MSFT", "company": "Microsoft Corporation", "price": 384.91, "change": 5.67, "change_percent": "1.49", "status": "success"},
        {"symbol": "GOOGL", "company": "Alphabet Inc.", "price": 141.25, "change": -1.83, "change_percent": "-1.28", "status": "success"},
        {"symbol": "NVDA", "company": "NVIDIA Corporation", "price": 441.78, "change": 12.34, "change_percent": "2.87", "status": "success"},
        {"symbol": "AMZN", "company": "Amazon.com Inc.", "price": 145.23, "change": 0.89, "change_percent": "0.62", "status": "success"},
        {"symbol": "TSLA", "company": "Tesla Inc.", "price": 238.45, "change": -4.21, "change_percent": "-1.74", "status": "success"}
    ]