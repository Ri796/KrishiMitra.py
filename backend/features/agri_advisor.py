# backend/features/agri_advisor.py

import json
import requests
from backend.features import weather
from backend.features import location_info
from backend.features import rule_engine # Will use the new stage-aware version
from backend import config

# ADD THIS BLOCK AT THE TOP OF THE FILE
import os
from dotenv import load_dotenv

# This command finds and loads your .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# This check confirms if the key was loaded
if not GEMINI_API_KEY:
    print(f"---!!! CRITICAL ERROR in {__file__}: GOOGLE_API_KEY not found. Check .env file. !!!---")
else:
    print(f"--- SUCCESS in {__file__}: Google API Key loaded. ---")
async def generate_agri_advice(city: str, state: str, crop: str, crop_stage: str, lang: str = 'en'):
    """
    Generates farming advice that is now aware of the crop's growth stage.
    """
    agro_climatic_zone = location_info.get_agro_climatic_zone_name(city, state)
    weather_data = weather.get_weather_data(city, state)
    if "error" in weather_data:
        return {"error": "Could not fetch weather data to generate advice."}

    # Call the upgraded rule engine with the crop_stage
    rule_based_advice = rule_engine.generate_rule_based_advice(weather_data, crop, crop_stage)

    # --- Upgraded Prompt Engineering with Crop Stage ---
    prompt = f"""
    You are an expert AI agronomist for Indian farmers. Your task is to convert structured advice into a simple, conversational summary and add productivity tips.

    CRITICAL INSTRUCTION: You MUST generate your entire response in the language with the code '{lang}'.

    **Context:**
    - Location: {city}, {state}, India
    - Agro-Climatic Zone (ACZ): {agro_climatic_zone}
    - Farmer's Crop: {crop}
    - Current Crop Stage: {crop_stage}
    - Current Weather: {json.dumps(weather_data)}
    - Structured Advice Points: {json.dumps(rule_based_advice)}

    **Instructions:**
    1.  Summarize the most critical advice from the structured points in simple, bullet-point format.
    2.  After the summary, add a new section called 'Productivity Tips'.
    3.  In the 'Productivity Tips' section, provide one additional, general tip for the specified '{crop}' at its current '{crop_stage}' to help increase yield or quality.
    4.  Keep the language simple and direct. Use emojis.
    """

    api_key = config.GEMINI_API_KEY 
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    payload = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
    # --- Call the Gemini AI Model ---
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    
    payload = {"contents": messages} # Assuming 'messages' is the variable holding your prompt

    try:
        # ADDED TIMEOUT and detailed error handling
        response = requests.post(api_url, json=payload, headers={'Content-Type': 'application/json'}, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        # Safely parse the response
        ai_response = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "Could not generate a valid plan.")
        
        # We assume the AI gives a JSON-like string that we need to parse
        # This is a placeholder; the real parsing might be more complex
        import json
        plan_data = json.loads(ai_response)
        return {"plan": plan_data}

    except requests.exceptions.Timeout:
        print(f"---!!! BACKEND AI ERROR in {__file__}!!!--- : The request to Google AI timed out.")
        return {"error": "AI service timed out. Please try again."}
    except requests.exceptions.RequestException as e:
        print(f"---!!! BACKEND AI ERROR in {__file__}!!!---")
        print(f"An exception occurred: {e}")
        if e.response is not None:
            print(f"Response from server: {e.response.text}")
        return {"error": "Could not connect to AI service. Check backend logs."}

    return {
        "agro_climatic_zone": agro_climatic_zone,
        "live_weather": weather_data,
        "ai_summary": ai_summary.strip()
    }
