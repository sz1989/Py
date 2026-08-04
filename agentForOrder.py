import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. Load your hidden API key from the .env file
load_dotenv()

# 2. Keep the backend tools exactly the same
def check_order_status(order_id: str) -> str:
    """Looks up the shipping status of a customer order using its ID number."""
    mock_database = {
        "12345": "Shipped yesterday via FedEx. Tracking number: 987654321.",
        "54321": "Processing in warehouse. Expected shipping date: Tomorrow."
    }
    return mock_database.get(order_id, f"Order ID {order_id} not found in system.")

def escalate_to_human(reason: str) -> str:
    """Alerts a human supervisor that a customer needs urgent assistance."""
    return f"[SYSTEM ALERT] Customer ticket successfully escalated to human team. Reason given: {reason}"

# 3. Initialize the modern Gemini Client
client = genai.Client()

# 4. Agent instructions (System Guidelines)
agent_instructions = """
You are an advanced customer support agent for an online retailer. 
Be polite, professional, and helpful. 
Use your tools to solve problems. If a customer is furious, aggressive, or demands 
to speak to a manager, immediately use the escalate_to_human tool.
"""

agent_tools = [check_order_status, escalate_to_human]

print("--- AI Support Agent Live ---")
# 5. Capture dynamic input from you right inside the terminal!
user_issue = input("Type your customer support question here: ")

print("\nAgent is processing your request using gemini-3.6-flash...")

# 6. Execute using the newest gemini-3.6-flash orchestration engine
response = client.models.generate_content(
    model='gemini-3.6-flash',  # Updated version
    contents=user_issue,
    config=types.GenerateContentConfig(
        system_instruction=agent_instructions,
        tools=agent_tools
        # Note: Temperature is omitted here as it is deprecated in Gemini 3.6+
    )
)

print("\n--- Agent Support Response ---")
print(response.text)
