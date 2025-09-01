import os
from anthropic import Anthropic
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()

# Initialize Claude client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_financial_analysis(user_message: str, current_stocks: List[Dict] = None) -> str:
    """
    Get financial analysis from Claude based on user question and current stock data
    """
    
    # Create context about current stock prices
    stock_context = ""
    if current_stocks:
        stock_context = "Current stock prices:\n"
        for stock in current_stocks:
            if stock["status"] == "success":
                stock_context += f"- {stock['symbol']} ({stock['company']}): ${stock['price']} ({stock['change']:+.2f}, {stock['change_percent']}%)\n"
    
    # System prompt for Claude to act as a financial advisor
    system_prompt = """You are a knowledgeable financial assistant helping users analyze stocks and make investment decisions. 

Guidelines:
- Provide clear, concise analysis based on the data provided
- Include both opportunities and risks in your responses
- Keep responses under 150 words for chat interface
- Be helpful but remind users that this is not professional financial advice
- Use the current stock price data when relevant to the user's question
- Focus on practical insights rather than complex technical analysis"""

    # Combine user message with stock context
    full_message = f"{stock_context}\n\nUser question: {user_message}"
    
    try:
        # Send message to Claude
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            system=system_prompt,
            messages=[
                {"role": "user", "content": full_message}
            ]
        )
        
        return response.content[0].text
        
    except Exception as e:
        print(f"Error calling Claude API: {e}")
        return "I apologize, but I'm having trouble processing your request right now. Please try again in a moment."

def get_market_summary(stocks_data: List[Dict]) -> str:
    """
    Generate a market summary based on current stock performance
    """
    
    if not stocks_data or all(stock["status"] == "error" for stock in stocks_data):
        return "Unable to generate market summary due to data unavailability."
    
    # Count positive vs negative performers
    positive = sum(1 for stock in stocks_data if stock["status"] == "success" and float(stock["change"]) > 0)
    negative = sum(1 for stock in stocks_data if stock["status"] == "success" and float(stock["change"]) < 0)
    total = sum(1 for stock in stocks_data if stock["status"] == "success")
    
    # Find best and worst performers
    valid_stocks = [stock for stock in stocks_data if stock["status"] == "success"]
    if valid_stocks:
        best_performer = max(valid_stocks, key=lambda x: float(x["change_percent"]))
        worst_performer = min(valid_stocks, key=lambda x: float(x["change_percent"]))
        
        summary_prompt = f"""Based on these 6 major stocks, give a brief market summary:

{positive} stocks are up, {negative} stocks are down out of {total} total.
Best performer: {best_performer['symbol']} (+{best_performer['change_percent']}%)
Worst performer: {worst_performer['symbol']} ({worst_performer['change_percent']}%)

Provide a 2-3 sentence market outlook based on this data."""

        try:
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=150,
                messages=[
                    {"role": "user", "content": summary_prompt}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Error generating market summary: {e}")
            return f"Market mixed: {positive} stocks up, {negative} down. {best_performer['symbol']} leads at +{best_performer['change_percent']}%."
    
    return "Market data unavailable for summary."