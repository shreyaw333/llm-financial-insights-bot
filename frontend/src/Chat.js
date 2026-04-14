import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

function Chat({ stocks }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: "Hello! I can help you analyze any of these stocks or answer questions about the market. What would you like to know?"
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchHistory = async () => {
    setHistoryLoading(true);
    try {
      const response = await fetch('https://llm-financial-insights-bot-production.up.railway.app/history?session_id=default');
      const data = await response.json();
      setChatHistory(data);
    } catch (error) {
      console.error('Error fetching history:', error);
    } finally {
      setHistoryLoading(false);
    }
  };

  const clearHistory = async () => {
    try {
      await fetch('https://llm-financial-insights-bot-production.up.railway.app/history?session_id=default', {
        method: 'DELETE'
      });
      setChatHistory([]);
      setMessages([{
        id: 1,
        type: 'bot',
        content: "Hello! I can help you analyze any of these stocks or answer questions about the market. What would you like to know?"
      }]);
    } catch (error) {
      console.error('Error clearing history:', error);
    }
  };

  const handleShowHistory = () => {
    setShowHistory(true);
    fetchHistory();
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('https://llm-financial-insights-bot-production.up.railway.app/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: inputMessage })
      });

      if (!response.ok) throw new Error('Failed to get response from Claude');

      const data = await response.json();
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: data.response
      };

      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        type: 'bot',
        content: "I apologize, but I'm having trouble processing your request right now. Please try again in a moment."
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleQuickQuestion = (question) => {
    setInputMessage(question);
    inputRef.current?.focus();
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <div className="chat-title">AI Assistant</div>
        <div className="chat-subtitle">Ask me about any stock</div>
        <button
          onClick={handleShowHistory}
          style={{
            background: 'transparent',
            border: '1px solid #28a745',
            color: '#28a745',
            borderRadius: '12px',
            padding: '4px 12px',
            fontSize: '12px',
            cursor: 'pointer',
            marginTop: '6px'
          }}
        >
          📋 Chat History
        </button>
      </div>

      {/* History Popup */}
      {showHistory && (
        <div style={{
          position: 'fixed',
          top: 0, left: 0, right: 0, bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.5)',
          zIndex: 1000,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          <div style={{
            background: 'white',
            borderRadius: '16px',
            padding: '24px',
            width: '90%',
            maxWidth: '600px',
            maxHeight: '70vh',
            display: 'flex',
            flexDirection: 'column',
            gap: '16px'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3 style={{ margin: 0, color: '#1a1a1a' }}>📋 Chat History</h3>
              <button
                onClick={() => setShowHistory(false)}
                style={{ background: 'transparent', border: 'none', fontSize: '20px', cursor: 'pointer' }}
              >✕</button>
            </div>

            <div style={{ overflowY: 'auto', flex: 1, display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {historyLoading ? (
                <p style={{ textAlign: 'center', color: '#666' }}>Loading history...</p>
              ) : chatHistory.length === 0 ? (
                <p style={{ textAlign: 'center', color: '#666' }}>No chat history yet.</p>
              ) : (
                chatHistory.map((msg, index) => (
                  <div key={index} style={{
                    padding: '10px 14px',
                    borderRadius: '10px',
                    background: msg.role === 'user' ? '#28a745' : '#f0f7f0',
                    color: msg.role === 'user' ? 'white' : '#1a1a1a',
                    alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                    maxWidth: '80%'
                  }}>
                    <div style={{ fontSize: '11px', opacity: 0.7, marginBottom: '4px' }}>
                      {msg.role === 'user' ? 'You' : 'AI'} · {formatTimestamp(msg.timestamp)}
                    </div>
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                  </div>
                ))
              )}
            </div>

            <button
              onClick={clearHistory}
              style={{
                background: '#dc3545',
                color: 'white',
                border: 'none',
                borderRadius: '10px',
                padding: '10px',
                cursor: 'pointer',
                fontWeight: 'bold'
              }}
            >
              🗑️ Clear History
            </button>
          </div>
        </div>
      )}

      <div className="chat-messages">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.type}`}>
            {message.type === 'bot'
              ? <ReactMarkdown>{message.content}</ReactMarkdown>
              : message.content
            }
          </div>
        ))}

        {isLoading && (
          <div className="typing-indicator">
            <div className="typing-dots">
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <div className="quick-questions">
          <div className="quick-question" onClick={() => handleQuickQuestion('What\'s your market outlook?')}>
            Market outlook?
          </div>
          <div className="quick-question" onClick={() => handleQuickQuestion('Which stock should I buy today?')}>
            Best buy today?
          </div>
          <div className="quick-question" onClick={() => handleQuickQuestion('What are the current market risks?')}>
            Risk assessment
          </div>
        </div>

        <div className="chat-input-wrapper">
          <textarea
            ref={inputRef}
            className="chat-input"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about any stock or market trend..."
            rows="1"
            disabled={isLoading}
          />
          <button
            className="send-button"
            onClick={sendMessage}
            disabled={isLoading || !inputMessage.trim()}
          >
            →
          </button>
        </div>
      </div>
    </div>
  );
}

export default Chat;