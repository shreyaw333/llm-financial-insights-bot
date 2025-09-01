import React, { useState, useRef, useEffect } from 'react';

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
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Send message to Claude
  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage
    };

    // Add user message immediately
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('http://llm-financial-insights-bot-production.up.railway.app/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage
        })
      });

      if (!response.ok) {
        throw new Error('Failed to get response from Claude');
      }

      const data = await response.json();
      
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: data.response
      };

      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: "I apologize, but I'm having trouble processing your request right now. Please try again in a moment."
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Quick question handlers
  const handleQuickQuestion = (question) => {
    setInputMessage(question);
    inputRef.current?.focus();
  };

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <div className="chat-title">AI Assistant</div>
        <div className="chat-subtitle">Ask me about any stock</div>
      </div>
      
      <div className="chat-messages">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.type}`}>
            {message.content}
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
          <div 
            className="quick-question" 
            onClick={() => handleQuickQuestion('What\'s your market outlook?')}
          >
            Market outlook?
          </div>
          <div 
            className="quick-question"
            onClick={() => handleQuickQuestion('Which stock should I buy today?')}
          >
            Best buy today?
          </div>
          <div 
            className="quick-question"
            onClick={() => handleQuickQuestion('What are the current market risks?')}
          >
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