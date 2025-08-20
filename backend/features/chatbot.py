# backend/features/chatbot.py

import os
import json
import requests
from dotenv import load_dotenv

# --- 1. SECURELY LOAD API KEY ---
# This block will run once when the server starts.
# It finds the .env file in your main project folder and loads the key.
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# This is a crucial check to confirm the key was loaded.
# You will see this message in your backend terminal when the server starts.
if not GEMINI_API_KEY:
    print("---!!! CRITICAL ERROR in chatbot.py: GOOGLE_API_KEY not found. Check your .env file. !!!---")
else:
    print("--- SUCCESS in chatbot.py: Google API Key loaded successfully. ---")

# --- 2. HELPER FUNCTIONS ---

def load_knowledge_base():
    """Loads the agricultural rules from our JSON file to give the AI context."""
    # Note: This path assumes you run the server from the project's root folder.
    try:
        with open('backend/data/agri_knowledge.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # It's okay if this file doesn't exist, just return an empty dictionary.
        return {}

# --- 3. MAIN CHATBOT LOGIC ---

async def generate_chatbot_response(user_message: str, history: list = [], language: str = 'en'):
    """
    Generates a conversational response from the AI chatbot.
    """
    if not GEMINI_API_KEY:
        # If the key wasn't loaded, send back an immediate error.
        return {"response": "Error: The API key is not configured on the server. Please contact the administrator."}

    knowledge = load_knowledge_base()
    
    # System prompt to guide the AI's behavior.
    system_prompt = f"""
    You are 'KrishiMitra', an expert AI agronomist for Indian farmers. 
    Your goal is to provide specific, actionable, and scientifically-grounded advice.
    Respond ONLY in the requested language: '{language}'.
    Your advice must be practical for a small-scale farmer in India.
    Use simple language and bullet points for clarity.
    Knowledge Base for Your Reference: {json.dumps(knowledge)}
    """

    # Prepare the conversation history for the AI.
    messages = [{"role": "user", "parts": [{"text": system_prompt}]}]
    for entry in history:
        # Make sure history items are correctly formatted dictionaries
        if isinstance(entry, dict) and "role" in entry and "content" in entry:
             # Adapt to the Gemini format
            role = "user" if entry["role"] == "user" else "model"
            messages.append({"role": role, "parts": [{"text": entry["content"]}]})
    
    # Add the latest user message.
    messages.append({"role": "user", "parts": [{"text": user_message}]})

    # --- Call the Gemini AI Model ---
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    
    payload = {"contents": messages}

    try:
        # We added a timeout to prevent infinite loading.
        response = requests.post(api_url, json=payload, headers={'Content-Type': 'application/json'}, timeout=30)
        response.raise_for_status() # This will raise an error for 4xx or 5xx responses
        result = response.json()
        
        # Safely get the text from the response
        ai_response = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "I'm sorry, I couldn't generate a valid response. Please try rephrasing your question.")

    except requests.exceptions.Timeout:
        print("---!!! BACKEND AI ERROR !!!--- : The request to Google AI timed out.")
        ai_response = "Sorry, the AI is taking too long to respond. Please try again in a moment."
    except requests.exceptions.RequestException as e:
        # This will now print the REAL error message from Google.
        print("---!!! BACKEND AI ERROR !!!---")
        print(f"An exception occurred: {e}")
        if e.response is not None:
            print(f"Response from server: {e.response.text}")
        ai_response = "Sorry, I had trouble processing that. Please check the backend logs for details."

    return {"response": ai_response.strip()}