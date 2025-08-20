# backend/features/rule_engine.py

import json

def load_crop_conditions():
    """Loads the ideal crop conditions from our JSON file."""
    try:
        with open('backend/data/crop_conditions.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def generate_rule_based_advice(weather_data: dict, crop: str, crop_stage: str):
    """
    Generates a list of actionable advice points based on rules
    that are now aware of the crop's growth stage.
    """
    advice_list = []
    crop_conditions = load_crop_conditions()
    
    temp = weather_data.get("temperature_celsius", 0)
    humidity = weather_data.get("humidity_percent", 0)
    condition = weather_data.get("condition", "").lower()

    # --- Stage-Specific Rules ---

    # Rule for Sowing Stage
    if crop_stage.lower() == 'sowing':
        if "rain" in condition:
            advice_list.append({
                "emoji": "✅", "type": "positive",
                "text": "Light rain is forecasted, which is excellent for sowing as it provides necessary moisture for germination."
            })
        else:
            advice_list.append({
                "emoji": "💧", "type": "action_needed",
                "text": "No rain is expected. Ensure you irrigate the field before sowing to ensure good seed germination."
            })

    # Rule for Harvesting Stage
    if crop_stage.lower() == 'harvesting':
        if "rain" in condition or "thunderstorm" in condition:
            advice_list.append({
                "emoji": "⚠️", "type": "critical",
                "text": "CRITICAL: Rain is expected! Harvest your crop immediately to prevent damage and loss of quality."
            })
        else:
            advice_list.append({
                "emoji": "☀️", "type": "positive",
                "text": "Clear weather is forecasted, which is ideal for harvesting your crop."
            })

    # --- General Rules (can apply at any stage) ---
    
    # High Humidity Warning
    if humidity > 80:
        advice_list.append({
            "emoji": "💧", "type": "warning",
            "text": f"High humidity ({humidity}%) increases the risk of fungal diseases. Ensure good air circulation."
        })

    # Crop-Specific Temperature Check
    if crop in crop_conditions:
        ideal_temp = crop_conditions[crop]["ideal_temp_celsius"]
        if not (ideal_temp[0] <= temp <= ideal_temp[1]):
            advice_list.append({
                "emoji": "🌡️", "type": "warning",
                "text": f"The current temperature ({temp}°C) is outside the ideal range for {crop}."
            })

    if not advice_list:
        advice_list.append({
            "emoji": "👍", "type": "info",
            "text": "Weather conditions appear stable for the current crop stage. Continue standard practices."
        })

    return advice_list
