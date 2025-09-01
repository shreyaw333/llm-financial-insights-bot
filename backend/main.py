from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import uvicorn

from market_data import get_all_stocks, get_mock_stocks
from claude_service import get_financial_analysis, get_market_summary

# Create FastAPI app
app = FastAPI(title="Financial Insights Bot", version="1.0.0")

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://llm-financial-insights-bot.vercel.app"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Store current stock data (simple in-memory cache)
current_stocks_data = []

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Insights Bot API is running"}

@app.get("/stocks")
async def get_stocks() -> List[Dict]:
    """
    Get current stock prices for dashboard
    """
    global current_stocks_data
    
    try:
        # Try to get real data first
        stocks_data = get_all_stocks()
        
        # If all stocks failed to load, use mock data
        if all(stock["status"] == "error" for stock in stocks_data):
            print("Using mock data due to API issues")
            stocks_data = get_mock_stocks()
        
        # Update our cache
        current_stocks_data = stocks_data
        
        return stocks_data
        
    except Exception as e:
        print(f"Error in /stocks endpoint: {e}")
        # Return mock data if everything fails
        current_stocks_data = get_mock_stocks()
        return current_stocks_data

@app.post("/chat")
async def chat_with_claude(message: ChatMessage) -> ChatResponse:
    """
    Send message to Claude and get financial analysis response
    """
    try:
        if not message.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Get Claude's response with current stock context
        claude_response = get_financial_analysis(
            user_message=message.message,
            current_stocks=current_stocks_data
        )
        
        return ChatResponse(response=claude_response)
        
    except Exception as e:
        print(f"Error in /chat endpoint: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Sorry, I'm having trouble processing your request. Please try again."
        )

@app.get("/market-summary")
async def get_market_summary_endpoint() -> Dict:
    """
    Get AI-generated market summary based on current stocks
    """
    try:
        if not current_stocks_data:
            # Get fresh data if cache is empty
            await get_stocks()
        
        summary = get_market_summary(current_stocks_data)
        
        return {"summary": summary}
        
    except Exception as e:
        print(f"Error generating market summary: {e}")
        return {"summary": "Market summary unavailable at the moment."}

# Run the server
if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )