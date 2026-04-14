import React, { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './Dashboard';
import Chat from './Chat';

function App() {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch stocks data from backend
  const fetchStocks = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch('https://llm-financial-insights-bot-production.up.railway.app/stocks');
      if (!response.ok) {
        throw new Error('Failed to fetch stock data');
      }
      
      const stocksData = await response.json();
      setStocks(stocksData);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching stocks:', err);
    } finally {
      setLoading(false);
    }
  };

  // Load stocks on component mount
  useEffect(() => {
    fetchStocks();
  }, []);

  return (
    <div className="App">
      <div className="container">
        {/* Main Content */}
        <div className="main-content">
          <div className="header">
            <div className="title">Financial Insights Bot</div>
            <div className="subtitle">Get AI-powered stock analysis and market insights</div>
          </div>
          
          <div className="market-status-container">
            <div className="market-status">
              <div className="status-indicator"></div>
              <div className="status-text">Market Open - Live Prices</div>
            </div>
            <button className="refresh-button" onClick={fetchStocks} disabled={loading}>
              {loading ? 'Loading...' : 'Refresh Prices'}
            </button>
          </div>
          
          {error && (
            <div className="error-message">
              Error: {error}
            </div>
          )}
          
          <Dashboard stocks={stocks} loading={loading} />
        </div>
        
        {/* Chat Panel */}
        <Chat stocks={stocks} />
      </div>
    </div>
  );
}

export default App;