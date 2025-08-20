# backend/features/govt_schemes.py

import json
from typing import Optional

def load_schemes_data(language: str = 'en'):
    """
    Loads the government schemes data from a language-specific JSON file.
    """
    filename = f'backend/data/govt_schemes_{language}.json'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Warning: {filename} not found. Falling back to English.")
        try:
            with open('backend/data/govt_schemes_en.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

def check_eligibility(scheme: dict, farmer_profile: dict) -> bool:
    """
    Checks if a farmer is eligible for a given scheme based on their profile.
    """
    criteria = scheme.get("eligibility_criteria", {})
    
    # Check gender criteria
    if "gender" in criteria and farmer_profile.get("gender"):
        if criteria["gender"].lower() != farmer_profile["gender"].lower():
            return False
            
    # Check land holding criteria
    if "min_land_holding_acres" in criteria and farmer_profile.get("land_holding_acres"):
        if farmer_profile["land_holding_acres"] < criteria["min_land_holding_acres"]:
            return False
            
    # Check if the farmer is a loanee
    if "is_loanee" in criteria and farmer_profile.get("is_loanee") is not None:
        if criteria["is_loanee"] != farmer_profile["is_loanee"]:
            return False
            
    # If all checks pass, the farmer is eligible
    return True

def get_schemes_for_farmer(state: str, farmer_profile: dict, language: str = 'en'):
    """
    Retrieves a personalized list of government schemes a farmer is eligible for.
    """
    all_schemes_data = load_schemes_data(language)
    
    # Combine national and state-specific schemes into one list
    national_schemes = all_schemes_data.get("national_schemes", [])
    state_schemes = all_schemes_data.get("state_specific_schemes", {}).get(state.title(), [])
    all_available_schemes = national_schemes + state_schemes
    
    # Filter the schemes based on the farmer's profile
    eligible_schemes = [
        scheme for scheme in all_available_schemes 
        if check_eligibility(scheme, farmer_profile)
    ]
    
    if not eligible_schemes:
        return {"message": "Based on the provided profile, no specific schemes were found. Please check the general list."}
        
    return {
        "query": {
            "state": state,
            "language": language,
            "farmer_profile": farmer_profile
        },
        "eligible_schemes": eligible_schemes
    }
