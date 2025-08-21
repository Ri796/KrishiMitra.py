# backend/features/productivity_booster.py

import os
import json
import requests
from dotenv import load_dotenv

# --- 1. SECURELY LOAD API KEY ---
# This block runs once when the server starts.
# It finds the .env file in your main project folder and loads the key.
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# This is a crucial check to confirm the key was loaded.
# You will see this message in your backend terminal when the server starts.
if not GEMINI_API_KEY:
    print(f"---!!! CRITICAL ERROR in {__file__}: GOOGLE_API_KEY not found. Check .env file. !!!---")
else:
    print(f"--- SUCCESS in {__file__}: Google API Key loaded successfully. ---")

# --- 2. MAIN FUNCTION ---

async def generate_expert_advice(crop: str, crop_stage: str, problem_description: str, goal: str, lang: str):
    """
    Generates a detailed, multi-part productivity plan from the AI.
    """
    if not GEMINI_API_KEY:
        # If the key wasn't loaded, send back an immediate error.
        return {"error": "API Key is not configured on the server. Please contact the administrator."}

    # --- Construct the detailed prompt for the AI ---
    system_prompt = f"""
    You are 'KrishiMitra', a world-class AI agronomist for Indian farmers. 
    A farmer needs an expert action plan. Your task is to provide a detailed, actionable, and scientifically-grounded plan.

    **Farmer's Situation:**
    - Crop: {crop}
    - Crop Stage: {crop_stage}
    - Problem Description: {problem_description}
    - Primary Goal: {goal}

    **Your Instructions:**
    1.  **Respond ONLY in the requested language:** '{lang}'.
    2.  **Provide a 3-Part Plan:** Your response MUST be a valid JSON object with three keys: "diagnosis", "action_plan", and "preventative_measures".
    3.  **Diagnosis:** Provide a clear, concise diagnosis of the potential problem.
    4.  **Action Plan:** Provide a list of 3-5 specific, actionable steps the farmer should take.
    5.  **Preventative Measures:** Provide a list of 2-3 measures to prevent this problem in the future.
    6.  **Be Practical and Scientific:** Your advice must be practical for a small-scale Indian farmer.
    
    Example JSON Output:
    {{
      "diagnosis": "The symptoms suggest a possible case of Early Blight, a common fungal disease in tomatoes, likely aggravated by nutrient deficiency.",
      "action_plan": ["Immediately remove and destroy affected lower leaves.", "Apply a copper-based fungicide, following label instructions carefully.", "Provide a balanced fertilizer with phosphorus and potassium to boost plant immunity."],
      "preventative_measures": ["Ensure proper spacing between plants for good air circulation.", "Use mulch to prevent soil from splashing onto leaves."]
    }}
    """

    # --- Prepare the payload for the API call ---
    messages = [{"role": "user", "parts": [{"text": system_prompt}]}]
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": messages}

    # --- Call the API and handle the response robustly ---
    try:
        response = requests.post(api_url, json=payload, headers={'Content-Type': 'application/json'}, timeout=90)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        result = response.json()
        
        # Safely extract the AI's text response
        ai_response_text = result['candidates'][0]['content']['parts'][0]['text']
        
        # Clean the response to ensure it's valid JSON
        clean_json_text = ai_response_text.strip().replace("```json", "").replace("```", "").strip()
        
        # Parse the JSON string into a Python dictionary
        plan_data = json.loads(clean_json_text)
        
        # Return the structured plan
        return {"plan": plan_data}

    except requests.exceptions.Timeout:
        print(f"---!!! BACKEND AI ERROR in {__file__} !!!--- : The request to Google AI timed out.")
        return {"error": "AI service timed out. Please try again."}
    except Exception as e:
        print(f"---!!! BACKEND AI ERROR in {__file__} !!!---")
        print(f"An exception occurred: {e}")
        # In case of an error, try to get more details from the response
        if 'response' in locals() and hasattr(response, 'text'):
            print(f"Response from server: {response.text}")
        return {"error": "Could not connect to or parse response from AI service. Check backend logs for details."}