# test_api.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

print("--- Starting API Key and Network Test ---")

# Step 1: Load the .env file
print("Attempting to load .env file...")
load_dotenv()
print(".env file loaded.")

# Step 2: Get the API key from the environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Step 3: Check if the key was actually found
if not GOOGLE_API_KEY:
    print("\nCRITICAL FAILURE: GOOGLE_API_KEY not found in the environment.")
    print("Please make sure your .env file is in the main project folder and is named correctly.")
else:
    # We print only the first and last few characters to confirm it's loaded without showing the whole key
    print(f"\nSUCCESS: Found API Key starting with '{GOOGLE_API_KEY[:4]}' and ending with '{GOOGLE_API_KEY[-4:]}'.")
    
    # Step 4: Try to connect to the Google AI service
    print("\nConfiguring Google AI...")
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        print("Successfully configured. Sending a test prompt to the AI...")
        
        # Step 5: Send a simple prompt
        response = model.generate_content("Why is the sky blue?")
        
        print("\n--- TEST COMPLETE ---")
        print("SUCCESS! The AI responded.")
        print("\nAI Response:")
        print(response.text)

    except Exception as e:
        print("\n--- TEST FAILED ---")
        print("CRITICAL FAILURE: An error occurred while trying to connect to or use the Google AI API.")
        print("\nError Details:")
        print(e)

print("\n--- End of Test ---")