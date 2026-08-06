import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file  

api_key = os.getenv("GEMINI_API_KEY")  # Retrieve the API key from environment variables

# 1. Configure the library with your unique Google AI Studio API key
genai.configure(api_key=api_key)

# 2. Select the fast, lightweight Gemini Flash model
model = genai.GenerativeModel('gemini-3.6-flash')

# 3. Create the text you want the AI to look at
LONG_ARTICLE = """
Virtual environments are essential tools in modern Python development. 
They create isolated spaces on your computer for individual projects. 
This means each project can have its own specific libraries and versions 
installed without interfering with other projects or your global computer setup. 
For example, Project A can use an older version of a tool while Project B uses 
the absolute newest version simultaneously without causing crashes.
"""

# 4. Ask the AI a question combined with your text data
PROMPT = f"Summarize the following text into exactly 2 simple bullet points:\n{LONG_ARTICLE}"

print("Sending request to Gemini AI... Please wait...")

# 5. Send the request and print out the result
response = model.generate_content(PROMPT)
print("\n--- AI Summary Result ---")
print(response.text)
