# pip install langchain langchain-google-genai yfinance
import os
import yfinance as yf
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, ToolMessage
from dotenv import load_dotenv

# 1. Load your hidden API key from the .env file
load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-3.6-flash") # Updated version

@tool
def get_stock_price(ticker: str) -> str:
    """Get the current stock price for a publicly traded company. 
    Use for questions about current price, value, or quote. 
    Examples: AAPL, MSFT, TSLA, NVDA, AMZN. 
    """
    try:
        # Fetch ticker data safely
        info = yf.Ticker(ticker.upper()).info
        
        # Extract price with a default float value to prevent formatting errors
        price = info.get("currentPrice") or info.get("regularMarketPrice", 0.0)
        
        # Format output safely
        company_name = info.get('longName', ticker.upper())
        return f"{company_name}: ${price:.2f}"
        
    except Exception as e:
        return f"Error fetching {ticker}: {e}"

@tool
def get_company_summary(ticker: str) -> str:
    """Get a business description for a company. 
    What they do, their sector, their industry. NOT for price information. 
    Use ticker like AAPL, MSFT. 
    """
    try:
        info = yf.Ticker(ticker.upper()).info
        summary = info.get("longBusinessSummary", "No description available.")
        return f"{info.get('longName')} | {info.get('sector')} | {summary[:400]}…"
    except Exception as e:
        return f"Error fetching info for {ticker}: {e}"

# Build the tool library
tools = [get_stock_price, get_company_summary]
tool_map = {t.name: t for t in tools}

# Initialize Gemini with bound tools
# Temperature 0 enforces strict JSON structure extraction for tools
llm_with_tools = ChatGoogleGenerativeAI(
    model=MODEL_NAME, 
    temperature=0
).bind_tools(tools)

def ask(question: str) -> str:
    #This tells the AI: "Hey, a human typed this question!"
    msgs = [HumanMessage(content=question)]
    #The AI reads your question and decides what to do next. It stores its decision inside a variable called response.
    response = llm_with_tools.invoke(msgs)
    
    # If Gemini determines no tools are required, return straight text
    if not response.tool_calls:
        return response.content
        
    # Standard agent routing loop
    # Remember the conversation If the AI does need a tool (like looking up Tesla's stock price), 
    # it will tell us: "I need to run a tool." We add this note to our msgs list so we don't forget what the AI just said.
    msgs.append(response)  
    # Find the tool: It looks up your custom Python function (like get_stock_price) by its name
    # Run it: It runs your Python code using the details the AI provided (like the ticker "TSLA").
    # Save the answer: It takes the real-world answer (like Tesla, Inc.: $220.00) and packages it as a ToolMessage so the AI knows this is raw data from a computer.
    for call in response.tool_calls:
        result = tool_map[call["name"]].invoke(call["args"])
        msgs.append(ToolMessage(content=result, tool_call_id=call["id"]))
        
    # Send tool execution results back to Gemini for final compilation
    return llm_with_tools.invoke(msgs).content

# --- TEST EXECUTIONS VIA AGENT ROUTER ---
if __name__ == "__main__":
    print("--- Testing Agent Router Responses ---")
    print(ask("What's Tesla's current stock price?"))
    print("\n" + "="*40 + "\n")
    print(ask("Explain what Nvidia does in simple terms."))
    print("\n" + "="*40 + "\n")
    print(ask("Is Amazon a good investment based on its business model?"))
    print("\n" + "="*40 + "\n")

    # --- STANDALONE UNIT TESTS (WITHOUT LLM) ---
    print("--- Testing Tool Isolation Unit Tests ---")
    result_aapl = get_stock_price.invoke({"ticker": "AAPL"})
    print(result_aapl)
    
    result_msft = get_stock_price.invoke({"ticker": "MSFT"})
    print(result_msft)
    
    result_invalid = get_stock_price.invoke({"ticker": "INVALIDTICKER123"})
    print(result_invalid)
    
    result_summary = get_company_summary.invoke({"ticker": "AAPL"})
    print(result_summary)
