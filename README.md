# Financial Insights Bot

**Live Application: [https://llm-financial-insights-bot.vercel.app/](https://llm-financial-insights-bot.vercel.app/)**

An AI-powered financial analysis platform that provides real-time stock data and intelligent market insights through an interactive chat interface. Get instant analysis on major stocks with the power of Claude AI.

## Technologies Used

**Frontend:**
- React.js
- CSS3 for custom styling
- Vercel (deployment)

**Backend:**
- Python
- FastAPI
- Anthropic Claude API for AI analysis
- Alpha Vantage API for stock data
- Railway (deployment)

**Architecture:**
- RESTful API design
- Real-time data fetching
- CORS-enabled cross-origin communication

## Table of Contents
* [Overview](#overview)
* [Architecture](#architecture)
* [Features](#features)
* [System Setup](#system-setup)
* [API Endpoints](#api-endpoints)

## Overview

The Financial Insights Bot is designed to:

1. **Fetch Real-time Stock Data**: Retrieves current prices, changes, and percentages for major stocks (AAPL, MSFT, GOOGL, NVDA, AMZN, TSLA)
2. **AI-Powered Analysis**: Leverages Claude AI to provide intelligent insights and market analysis
3. **Interactive Chat Interface**: Allows users to ask questions about stocks and receive detailed responses
4. **Dashboard Visualization**: Displays current market status with live price updates

## Architecture

The system follows a modern full-stack architecture with clear separation of concerns:

1. **Frontend Layer (React + Vercel)**
   - React.js application for user interface
   - Real-time dashboard displaying stock data
   - Interactive chat component for AI conversations
   - Responsive design for mobile and desktop

2. **Backend Layer (FastAPI + Railway)**
   - FastAPI server handling API requests
   - Market data service for stock price retrieval
   - Claude AI service for natural language processing
   - Error handling and fallback mechanisms

3. **External APIs**
   - **Alpha Vantage API**: Real-time stock market data
   - **Anthropic Claude API**: AI-powered financial analysis
   - Fallback mock data for high availability

4. **Data Flow**
   - Frontend requests stock data from backend
   - Backend fetches real-time prices from Alpha Vantage
   - User queries are processed by Claude AI with stock context
   - Responses are delivered back through the chat interface

## Features

- **Real-time Stock Monitoring**: Live prices for major tech stocks
- **AI Chat Assistant**: Ask questions about market trends, specific stocks, or investment advice
- **Market Status Indicator**: Visual indication of market conditions
- **Quick Question Buttons**: Pre-defined queries for common analysis needs
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Error Handling**: Graceful fallbacks when external APIs are unavailable

## Use Cases

The Financial Insights Bot can help you make informed investment decisions by answering questions like:

**Individual Stock Analysis:**
- "Should I buy or sell my NVIDIA stock today?"
- "Is Apple a good buy at current levels?"
- "Should I buy Tesla or hold off for a better entry point?"
- "Should I sell Google at these levels or wait for recovery?"

**Market Comparison:**
- "Which is a better investment right now: Microsoft or Apple?"
- "Should I invest in NVIDIA or Amazon for long-term growth?"
- "Compare Tesla and Apple for the next quarter"

**Market Timing:**
- "Is this a good time to enter the tech market?"
- "Should I wait for a market dip before buying stocks?"
- "What's the market outlook for the next few weeks?"

**Risk Assessment:**
- "What are the current risks in holding tech stocks?"
- "How volatile is NVIDIA compared to other stocks?"
- "Which stocks are safest during market uncertainty?"

**Portfolio Strategy:**
- "Should I diversify away from tech stocks?"
- "What percentage of my portfolio should be in growth stocks?"
- "How should I rebalance my current holdings?"

## System Setup

**Prerequisites:**
- Node.js 16+ and npm
- Python 3.8+
- Alpha Vantage API key
- Anthropic Claude API key

**Backend Setup:**

1. Clone the repository
```bash
git clone <your-repo-url>
cd llm-financial-insights-bot
```

2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
# Create .env file with:
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
ANTHROPIC_API_KEY=your_claude_api_key
```

5. Run the FastAPI server
```bash
python main.py
```

**Frontend Setup:**

1. Navigate to frontend directory
```bash
cd frontend  # or wherever your React app is located
```

2. Install dependencies
```bash
npm install
```

3. Update API endpoint in your code to point to your backend

4. Run the development server
```bash
npm start
```

## API Endpoints

**GET /stocks**
- Returns current stock data for major companies
- Includes price, change, and percentage change
- Fallback to mock data if API fails

**POST /chat**
- Accepts user messages for AI analysis
- Returns Claude AI responses with stock context
- Body: `{"message": "your question here"}`

**GET /market-summary**
- Returns AI-generated market summary
- Based on current stock performance

**GET /**
- Health check endpoint
- Returns API status

---

**If this repository helped you, please give it a star!**