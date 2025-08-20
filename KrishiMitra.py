# ==============================================================================
# KrishiMitra: An AI-Powered Assistant for Farmers
#
# This Streamlit application provides multi-lingual support for various
# agricultural tools including fertilizer recommendations, loan eligibility,
# weather alerts, crop calendars, and live market prices.
#
# Refactored to address UI/UX improvements, fix critical bugs, and enhance
# security as per open-source contribution guidelines.
# ==============================================================================

import streamlit as st
from datetime import datetime
from gtts import gTTS
import base64
import os
import requests
import pandas as pd

# --- 1. CONFIGURATION & SETUP ---

# Securely load the API key from Streamlit's secrets management
# This prevents exposing the key in the public codebase.
try:
    API_KEY = st.secrets["OPENWEATHER_API_KEY"]
except (FileNotFoundError, KeyError):
    st.error("ERROR: API key not found. Please add it to your .streamlit/secrets.toml file.")
    st.stop()

# --- 2. CORE FUNCTIONS ---

def get_weather_details(city_name):
    """Fetches weather data from the OpenWeatherMap API for a given city."""
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&APPID={API_KEY}"
    response = requests.get(api_url)
    data = response.json()

    # Place raw JSON in a collapsible expander for debugging, not on the main UI.
    with st.expander("Show Raw API Response (for developers)"):
        st.json(data)

    if data.get('cod') == '404' or data.get('cod') != 200:
        return None, None, None
    else:
        weather = data['weather'][0]['main']
        temp = round(data['main']['temp'])
        humidity = data['main']['humidity']
        return weather, temp, humidity

def play_audio(text, lang_code='en'):
    """Generates and plays audio from text using Google Text-to-Speech."""
    try:
        tts = gTTS(text=text, lang=lang_code)
        filename = "temp_audio.mp3"
        tts.save(filename)

        with open(filename, "rb") as audio_file:
            audio_bytes = audio_file.read()
        
        b64 = base64.b64encode(audio_bytes).decode()
        audio_html = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
        
        st.markdown(audio_html, unsafe_allow_html=True)
        os.remove(filename)
    except Exception as e:
        st.error(f"Could not play audio. Error: {e}")

# --- 3. LANGUAGE & STATIC DATA ---

# Central dictionary for multi-language support.
LANGUAGE_DATA = {
    "English": {"welcome": "🌾 Welcome to KrishiMitra!", "fertilizer": "🌱 Fertilizer Recommendation", "loan": "🏦 Loan/Subsidy Checker", "weather_alert": "🌦️ Weather Alerts", "crop_calendar": "📅 Crop Calendar", "mandi_prices": "📊 Mandi Prices", "tts_lang": "en"},
    "Hindi": {"welcome": "🌾 कृषि मित्र में आपका स्वागत है!", "fertilizer": "🌱 उर्वरक सिफारिश", "loan": "🏦 ऋण/सब्सिडी जांच", "weather_alert": "🌦️ मौसम अलर्ट", "crop_calendar": "📅 फसल कैलेंडर", "mandi_prices": "📊 मंडी की कीमतें", "tts_lang": "hi"},
    "Bhojpuri": {"welcome": "🌾 कृषिमित्र में रउआ स्वागत बा!", "fertilizer": "🌱 खाद सिफारिश", "loan": "🏦 कर्ज/सब्सिडी जांच", "weather_alert": "🌦️ मौसम चेतावनी", "crop_calendar": "📅 फसल कैलेंडर", "mandi_prices": "📊 मंडी के दाम", "tts_lang": "hi"},
    # ... (Add other languages as before) ...
    "Marathi": {"welcome": "🌾 कृषिमित्र मध्ये तुमचं स्वागत आहे!", "fertilizer": "🌱 खत शिफारस", "loan": "🏦 कर्ज/अनुदान तपासणी", "weather_alert": "🌦️ हवामान इशारा", "crop_calendar": "📅 पीक दिनदर्शिका", "mandi_prices": "📊 मंडी भाव", "tts_lang": "mr"}
}

# Static data for Mandi prices (ideally, this would come from an API).
MANDI_DATA = {
    "Wheat": 2200, "Rice": 1800, "Mustard": 5500, "Maize": 1700, "Barley": 1600,
    "Soybean": 4800, "Cotton": 6600, "Sugarcane": 340, "Potato": 1200, "Tomato": 1100
}

# --- 4. UI: SIDEBAR (for all user inputs) ---

st.sidebar.title("⚙️ Controls")

# Language selection is the primary control.
language = st.sidebar.selectbox("🌐 Select Language", list(LANGUAGE_DATA.keys()))
lang_content = LANGUAGE_DATA[language]

# Fertilizer Recommendation Inputs
st.sidebar.header(lang_content["fertilizer"])
crop = st.sidebar.selectbox("Select Crop", ["Wheat", "Rice", "Maize", "Sugarcane", "Potato", "Tomato"])
soil = st.sidebar.selectbox("Soil Type", ["Black", "Red", "Sandy", "Brown"])

# Loan/Subsidy Checker Inputs
st.sidebar.header(lang_content["loan"])
age = st.sidebar.number_input("Enter your age", min_value=18, max_value=80)
holding = st.sidebar.selectbox("Land holding (acres)", ["<1", "1-5", ">5"])

# Weather Alerts Inputs
st.sidebar.header(lang_content["weather_alert"])
user_city = st.sidebar.text_input('Enter your city')

# Crop Calendar Inputs
st.sidebar.header(lang_content["crop_calendar"])
season = st.sidebar.selectbox("Choose Season", ["Rabi", "Kharif", "Zaid"])


# --- 5. UI: MAIN PAGE (for all outputs, organized in tabs) ---

st.title(lang_content["welcome"])
if st.button("🔊 Read Welcome Message"):
    play_audio(lang_content["welcome"], lang_content["tts_lang"])

# Initialize session state for storing results to fix the nested button bug.
if 'fertilizer_rec' not in st.session_state: st.session_state.fertilizer_rec = ""
if 'loan_eligibility' not in st.session_state: st.session_state.loan_eligibility = ""
if 'calendar_info' not in st.session_state: st.session_state.calendar_info = ""

# Create tabs for a clean, organized layout.
tab_rec, tab_weather, tab_calendar, tab_prices = st.tabs([
    "🌱 Recommendations & Schemes", 
    lang_content["weather_alert"], 
    lang_content["crop_calendar"], 
    lang_content["mandi_prices"]
])

# == Recommendations Tab ==
with tab_rec:
    st.header(lang_content["fertilizer"])
    if st.sidebar.button("Get Recommendation"):
        # Set the result in session state instead of displaying it directly.
        st.session_state.fertilizer_rec = f"For {crop} in {soil} soil, use NPK 20:20:0 at 50kg/acre."

    # Display and play audio only if a result exists in the session state.
    if st.session_state.fertilizer_rec:
        st.success(st.session_state.fertilizer_rec)
        if st.button("🔊 Listen Recommendation"):
            play_audio(st.session_state.fertilizer_rec, lang_content["tts_lang"])

    st.markdown("---")
    st.header(lang_content["loan"])
    if st.sidebar.button("Check Eligibility"):
        st.session_state.loan_eligibility = "You are eligible for KCC and PM-KISAN schemes."

    if st.session_state.loan_eligibility:
        st.info(st.session_state.loan_eligibility)
        if st.button("🔊 Listen Eligibility"):
            play_audio(st.session_state.loan_eligibility, lang_content["tts_lang"])

# == Weather Tab ==
with tab_weather:
    st.header(lang_content["weather_alert"])
    st.write(f"Today's Date: {datetime.now().strftime('%d-%m-%Y')}")
    if st.sidebar.button('Check Weather'):
        if user_city:
            weather, temp, humidity = get_weather_details(user_city)
            if weather:
                # Use st.metric for a much cleaner, professional display.
                col1, col2, col3 = st.columns(3)
                col1.metric("Temperature", f"{temp}°F")
                col2.metric("Condition", weather)
                col3.metric("Humidity", f"{humidity}%")
            else:
                st.error("City not found. Please check the name and try again.")
        else:
            st.warning("Please enter a city name in the sidebar.")

# == Crop Calendar Tab ==
with tab_calendar:
    st.header(lang_content["crop_calendar"])
    if st.sidebar.button("Show Calendar"):
        st.session_state.calendar_info = f"For the {season} season, recommended crops to sow are Wheat, Mustard, and Barley."

    if st.session_state.calendar_info:
        st.success(st.session_state.calendar_info)
        if st.button("🔊 Listen Calendar"):
            play_audio(st.session_state.calendar_info, lang_content["tts_lang"])

# == Mandi Prices Tab ==
with tab_prices:
    st.header(lang_content["mandi_prices"])
    
    # Convert data to a pandas DataFrame for visualization.
    df = pd.DataFrame(list(MANDI_DATA.items()), columns=['Crop', 'Price (₹ per qtl)'])
    
    st.info("Displaying average prices per quintal (qtl). Prices may vary by location.")
    
    # Use st.bar_chart for an interactive visual.
    st.bar_chart(df.set_index('Crop'))
    
    # Keep the raw table in an expander for those who want details.
    with st.expander("View as a Table"):
        st.table(df)

# --- 6. FOOTER ---
st.markdown("---")
st.markdown("Made with ❤️ for Indian Farmers - **KrishiMitra 2.0**")