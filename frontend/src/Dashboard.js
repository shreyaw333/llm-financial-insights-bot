import React from 'react';

function Dashboard({ stocks, loading }) {
  if (loading) {
    return (
      <div className="stocks-grid">
        {[...Array(6)].map((_, index) => (
          <div key={index} className="stock-card loading">
            <div className="loading-content">Loading...</div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="stocks-grid">
      {stocks.map((stock) => (
        <StockCard key={stock.symbol} stock={stock} />
      ))}
    </div>
  );
}

function StockCard({ stock }) {
  const isPositive = parseFloat(stock.change) > 0;
  const changeClass = isPositive ? 'positive' : 'negative';
  const changeSymbol = isPositive ? '+' : '';

  return (
    <div className="stock-card">
      <div className="stock-header">
        <div className="stock-symbol">{stock.symbol}</div>
      </div>
      <div className="stock-company">{stock.company}</div>
      <div className="stock-price">${stock.price}</div>
      <div className={`stock-change ${changeClass}`}>
        {changeSymbol}${stock.change} ({changeSymbol}{stock.change_percent}%)
      </div>
      {stock.status === 'error' && (
        <div className="error-indicator">Data unavailable</div>
      )}
    </div>
  );
}

export default Dashboard;