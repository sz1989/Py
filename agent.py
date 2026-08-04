import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. Load your hidden API key from the .env file
load_dotenv()

# 2. Define a "Tool" function that the AI Agent can choose to run
def list_my_files() -> str:
    """
    Lists all files in the user's current project directory.
    Returns a string containing the filenames.
    """
    try:
        # Get the files in the folder where this script is running
        files = os.listdir('.')
        return f"The files in the current directory are: {', '.join(files)}"
    except Exception as e:
        return f"Error reading directory: {str(e)}"

# 3. Initialize the client (automatically finds GEMINI_API_KEY from memory)
client = genai.Client()

# 4. Define the Agent's identity, system instructions, and available tools
agent_instructions = "You are a helpful Mac desktop assistant. Use your tools to answer the user's request accurately."
agent_tools = [list_my_files]

# 5. Give the Agent an instruction that requires using a tool
user_prompt = "Hey! Can you check my current project directory and let me know if there are any hidden configuration files inside?"

print(f"User Request: '{user_prompt}'\n")
print("Agent is thinking and selecting tools...")

# 6. Run the agent using the automatic function-calling model configuration
response = client.models.generate_content(
    model='gemini-3.6-flash', # This specific workflow uses the core developer engine
    contents=user_prompt,
    config=types.GenerateContentConfig(
        system_instruction=agent_instructions,
        tools=agent_tools,
        temperature=0.1 # Low temperature keeps the agent focused and logical
    )
)

# 7. Print the final reasoning and summary from the agent
print("\n--- Agent Final Response ---")
print(response.text)
