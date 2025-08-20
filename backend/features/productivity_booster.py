# backend/features/productivity_booster.py

import json
import requests
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

async def generate_expert_advice(crop: str, crop_stage: str, problem_description: str, goal: str, lang: str = 'en'):
    """
    Generates an expert, multi-part advisory plan using an advanced AI prompt.
    """
    # --- Advanced Prompt Engineering ---
    prompt = f"""
    You are 'KrishiNet', a world-class AI agronomist. Your task is to provide a detailed, actionable plan for a farmer based on their specific situation.

    **CRITICAL INSTRUCTION: You MUST generate your entire response in the language with the code '{lang}'.**

    **Farmer's Situation:**
    - Crop: {crop}
    - Current Crop Stage: {crop_stage}
    - Problem Description: "{problem_description}"
    - Farmer's Goal: {goal}

    **Your Task:**
    Generate a structured response with the following four sections, in this exact order:

    1.  **Disease/Problem Diagnosis:**
        - Based on the problem description, what is the most likely disease, pest, or deficiency?
        - State your confidence level (e.g., "Likely," "Possibly").

    2.  **Organic Solutions:**
        - Provide 2-3 specific, actionable organic remedies.
        - Example: "Prepare a neem oil solution (10ml per liter of water) and spray on the affected leaves in the evening."

    3.  **Chemical Solutions (Pesticides/Fungicides):**
        - Recommend 1-2 specific chemical compounds (e.g., "Mancozeb," "Imidacloprid").
        - **IMPORTANT:** Include a strong warning to check the product label for correct dosage and safety precautions.

    4.  **Productivity Boosters:**
        - Provide 1-2 tips directly related to the farmer's goal ('{goal}') for this specific '{crop}' at its current '{crop_stage}'.
        - Example for 'Increase Yield': "At the flowering stage, consider a foliar spray of a balanced NPK fertilizer (like 19-19-19) to boost fruit development."

    Format the entire output clearly. Use emojis.
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
    return {"expert_plan": ai_plan.strip()}
