import requests

# We must add a 'User-Agent' header so the website knows we are a Python script
headers = {
    "Accept": "application/json",
    "User-Agent": "MyPythonLearningScript/1.0"
}

response = requests.get("https://icanhazdadjoke.com", headers=headers)

if response.status_code == 200:
    try:
        # Convert to a Python dictionary
        joke_data = response.json()
        print(joke_data["joke"])
        
    except Exception as e:
        print("Failed to parse JSON data.")
        print(f"Raw response text was: {response.text}")
else:
    print(f"Could not connect. Status code: {response.status_code}")
