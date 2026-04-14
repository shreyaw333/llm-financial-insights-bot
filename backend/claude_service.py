import os
from anthropic import Anthropic
from dotenv import load_dotenv
from typing import Dict, List
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.messages import HumanMessage, AIMessage
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
conversation_memories = {}

def get_db_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')

def init_db():
    """Create chat_history table if it doesn't exist"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id SERIAL PRIMARY KEY,
                session_id VARCHAR(255),
                role VARCHAR(50),
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database init error: {e}")

# Initialize DB on startup
init_db()

def get_or_create_memory(session_id: str = "default") -> ConversationBufferWindowMemory:
    if session_id not in conversation_memories:
        conversation_memories[session_id] = ConversationBufferWindowMemory(
            k=10,
            return_messages=True
        )
    return conversation_memories[session_id]

def save_message_to_db(session_id: str, role: str, content: str):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chat_history (session_id, role, content) VALUES (%s, %s, %s)",
            (session_id, role, content)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error saving to DB: {e}")

def get_history_from_db(session_id: str = "default") -> List[Dict]:
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "SELECT role, content, timestamp FROM chat_history WHERE session_id = %s ORDER BY timestamp ASC",
            (session_id,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error fetching from DB: {e}")
        return []

def clear_history_from_db(session_id: str = "default"):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM chat_history WHERE session_id = %s", (session_id,))
        conn.commit()
        cur.close()
        conn.close()
        # Also clear in-memory
        if session_id in conversation_memories:
            del conversation_memories[session_id]
    except Exception as e:
        print(f"Error clearing DB: {e}")

def get_financial_analysis(user_message: str, current_stocks: List[Dict] = None, session_id: str = "default") -> str:
    memory = get_or_create_memory(session_id)

    stock_context = ""
    if current_stocks:
        stock_context = "Current stock prices:\n"
        for stock in current_stocks:
            if stock["status"] == "success":
                stock_context += f"- {stock['symbol']} ({stock['company']}): ${stock['price']} ({stock['change']:+.2f}, {stock['change_percent']}%)\n"

    history = memory.load_memory_variables({})
    history_text = ""
    if history.get("history"):
        for msg in history["history"]:
            if isinstance(msg, HumanMessage):
                history_text += f"User: {msg.content}\n"
            elif isinstance(msg, AIMessage):
                history_text += f"Assistant: {msg.content}\n"

    system_prompt = """You are a knowledgeable financial assistant helping users analyze stocks and make investment decisions.

Guidelines:
- Provide clear, concise analysis based on the data provided
- Include both opportunities and risks in your responses
- Keep responses under 150 words for chat interface
- Be helpful but remind users that this is not professional financial advice
- Use the current stock price data when relevant to the user's question
- Remember context from earlier in the conversation
- Focus on practical insights rather than complex technical analysis"""

    full_message = f"{stock_context}\n\nConversation so far:\n{history_text}\nUser question: {user_message}"

    try:
        response = client.messages.create(
            model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5"),
            max_tokens=300,
            system=system_prompt,
            messages=[{"role": "user", "content": full_message}]
        )

        answer = response.content[0].text
        memory.save_context({"input": user_message}, {"output": answer})
        
        # Save both messages to PostgreSQL
        save_message_to_db(session_id, "user", user_message)
        save_message_to_db(session_id, "assistant", answer)

        return answer

    except Exception as e:
        print(f"Error calling Claude API: {e}")
        return "I apologize, but I'm having trouble processing your request right now. Please try again in a moment."


def get_market_summary(stocks_data: List[Dict]) -> str:
    if not stocks_data or all(stock["status"] == "error" for stock in stocks_data):
        return "Unable to generate market summary due to data unavailability."

    positive = sum(1 for stock in stocks_data if stock["status"] == "success" and float(stock["change"]) > 0)
    negative = sum(1 for stock in stocks_data if stock["status"] == "success" and float(stock["change"]) < 0)
    total = sum(1 for stock in stocks_data if stock["status"] == "success")

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
                model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5"),
                max_tokens=150,
                messages=[{"role": "user", "content": summary_prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error generating market summary: {e}")
            return f"Market mixed: {positive} stocks up, {negative} down. {best_performer['symbol']} leads at +{best_performer['change_percent']}%."

    return "Market data unavailable for summary."