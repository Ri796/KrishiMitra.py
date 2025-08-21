import streamlit as st
from datetime import datetime
from gtts import gTTS
import base64
import os
import requests
import pandas as pd

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(
    page_title="KrishiMitra",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Securely load the API key from Streamlit's secrets management
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except (FileNotFoundError, KeyError):
    st.error("ERROR: API key not found. Please add a .streamlit/secrets.toml file with your key.")
    st.stop()

# --- 2. CORE FUNCTIONS ---
def get_weather_details(city_name):
    """Fetches weather data from the OpenWeatherMap API for a given city."""
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&APPID={API_KEY}"
    response = requests.get(api_url)
    data = response.json()
    if data.get('cod') != 200:
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
# This is the main dictionary for all translated text
LANGUAGE_DATA = {
    "en": {"welcome": "Welcome to KrishiMitra!", "fertilizer": "Fertilizer Recommendation", "loan": "Loan & Subsidy Checker", "weather_alert": "Weather Alerts", "crop_calendar": "Crop Calendar", "mandi_prices": "Mandi Prices", "tts_lang": "en"},
    "hi": {"welcome": "कृषि मित्र में आपका स्वागत है!", "fertilizer": "उर्वरक सिफारिश", "loan": "ऋण/सब्सिडी जांच", "weather_alert": "मौसम अलर्ट", "crop_calendar": "फसल कैलेंडर", "mandi_prices": "मंडी की कीमतें", "tts_lang": "hi"},
    "bn": {"welcome": "কৃষি মিত্র-তে স্বাগতম!", "fertilizer": "সার সুপারিশ", "loan": "ঋণ/ভর্তুকি যাচাই", "weather_alert": "আবহাওয়ার সতর্কবার্তা", "crop_calendar": "ফসল ক্যালেন্ডার", "mandi_prices": "মান্ডির দাম", "tts_lang": "bn"},
    "as": {"welcome": "কৃষি মিত্ৰলৈ স্বাগতম!", "fertilizer": "সাৰৰ পৰামৰ্শ", "loan": "ঋণ/ৰাজসাহায্য পৰীক্ষক", "weather_alert": "বতৰৰ সতৰ্কবাণী", "crop_calendar": "শস্যৰ কেলেণ্ডাৰ", "mandi_prices": "মন্দিৰ দৰ", "tts_lang": "as"},
    "or": {"welcome": "କୃଷି ମିତ୍ରରେ ସ୍ଵାଗତ!", "fertilizer": "ସାର ସୁପାରିଶ", "loan": "ଋଣ/ସବସିଡି ଯାଞ୍ଚ", "weather_alert": "ପାଣିପାଗ ସତର୍କତା", "crop_calendar": "ଫସଲ କ୍ୟାଲେଣ୍ଡର", "mandi_prices": "ମଣ୍ଡି ଦର", "tts_lang": "or"},
    "te": {"welcome": "కృషిమిత్రా కు స్వాగతం!", "fertilizer": "ఎరువు సిఫార్సు", "loan": "రుణం/సబ్సిడీ తనిఖీ", "weather_alert": "వాతావరణ హెచ్చరికలు", "crop_calendar": "పంట క్యాలెండర్", "mandi_prices": "మండి ధరలు", "tts_lang": "te"},
    "mr": {"welcome": "कृषिमित्र मध्ये तुमचं स्वागत आहे!", "fertilizer": "खत शिफारस", "loan": "कर्ज/अनुदान तपासणी", "weather_alert": "हवामान इशारा", "crop_calendar": "पीक दिनदर्शिका", "mandi_prices": "मंडी भाव", "tts_lang": "mr"},
    "ta": {"welcome": "கிருஷிமித்ராவிற்கு வரவேற்கிறோம்!", "fertilizer": "உர பரிந்துரை", "loan": "கடன்/தொகை சரிபார்ப்பு", "weather_alert": "வானிலை எச்சரிக்கை", "crop_calendar": "பயிர் நாட்காட்டி", "mandi_prices": "மண்டி விலைகள்", "tts_lang": "ta"},
    "gu": {"welcome": "કૃષિમિત્ર માં આપનું સ્વાગત છે!", "fertilizer": "ખાતર ભલામણ", "loan": "લોન/સબસિડી તપાસ", "weather_alert": "હવામાન ચેતવણી", "crop_calendar": "પાક કેલેન્ડર", "mandi_prices": "મંડીના ભાવ", "tts_lang": "gu"},
    "kn": {"welcome": "ಕೃಷಿ ಮಿತ್ರಕ್ಕೆ ಸ್ವಾಗತ!", "fertilizer": "ರಸಗೊಬ್ಬರ ಶಿಫಾರಸು", "loan": "ಸಾಲ/ಸಬ್ಸಿಡಿ ತಪಾಸಣೆ", "weather_alert": "ಹವಾಮಾನ ಎಚ್ಚರಿಕೆ", "crop_calendar": "ಬೆಳೆ ದಿನದರ್ಶಿ", "mandi_prices": "ಮಂಡಿ ಬೆಲೆಗಳು", "tts_lang": "kn"},
    "pa": {"welcome": "ਕ੍ਰਿਸ਼ੀ ਮਿਤਰ ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ!", "fertilizer": "ਖਾਦ ਸਿਫਾਰਸ਼", "loan": "ਕਰਜ਼ਾ ਜਾਂ ਸਬਸਿਡੀ ਚੈੱਕਰ", "weather_alert": "ਮੌਸਮ ਚੇਤਾਵਨੀ", "crop_calendar": "ਫਸਲ ਕੈਲੰਡਰ", "mandi_prices": "ਮੰਡੀ ਦੀਆਂ ਕੀਮਤਾਂ", "tts_lang": "pa"},
    "ml": {"welcome": "കൃഷി മിത്രയിലേക്ക് സ്വാഗതം!", "fertilizer": "വളം ശുപാർശ", "loan": "വായ്പ/സബ്സിഡി പരിശോധന", "weather_alert": "കാലാവസ്ഥാ മുന്നറിയിപ്പ്", "crop_calendar": "വിള കലണ്ടർ", "mandi_prices": "മണ്ഡി വിലകൾ", "tts_lang": "ml"},
    "tcy": {"welcome": "ಕೃಷಿ ಮಿತ್ರೆಗ್ ಸ್ವಾಗತ!", "fertilizer": "ಗೊಬ್ಬರದ ಸಲಹೆ", "loan": "ಸಾಲ/ಸಬ್ಸಿಡಿ ತಪಾಸಣೆ", "weather_alert": "ಹವಾಮಾನ ಎಚ್ಚರಿಕೆ", "crop_calendar": "ಬೆಳೆ ದಿನಚರಿ", "mandi_prices": "ಮಂಡಿದ ಬೆಲೆಕುಲು", "tts_lang": "en"},
    "mni": {"welcome": "কৃষি মিত্রদা তরাম্না ওকচরি!", "fertilizer": "হাওয়াই থুম শিজিনবগী পাওতাক", "loan": "লোন/সবসিডি চেক তৌবা", "weather_alert": "নোংগী পাও", "crop_calendar": "মহৈ-মরোংগী ক্যালেন্ডার", "mandi_prices": "মন্দিগী মমল", "tts_lang": "en"}
}

MANDI_DATA = { "Wheat": 2200, "Rice": 1800, "Mustard": 5500, "Maize": 1700, "Barley": 1600 }

# --- 4. UI: SIDEBAR (Corrected Version) ---
with st.sidebar:
    st.title("⚙️ Controls")

    # --- SIMPLIFIED LANGUAGE SELECTION ---
    # We now create the display names and get the language code directly
    # from the main LANGUAGE_DATA dictionary. No need for a separate dictionary.
    
    # Create user-friendly names for the dropdown, e.g., "English (en)"
    language_display_names = {
        "English (en)": "en", "हिन्दी (hi)": "hi", "বাংলা (bn)": "bn", "অসমীয়া (as)": "as",
        "ଓଡ଼ିଆ (or)": "or", "తెలుగు (te)": "te", "मराठी (mr)": "mr", "தமிழ் (ta)": "ta",
        "ગુજરાતી (gu)": "gu", "ಕನ್ನಡ (kn)": "kn", "ਪੰਜਾਬੀ (pa)": "pa",
        "മലയാളം (ml)": "ml", "ತುಳು (tcy)": "tcy", "মণিপুরী (mni)": "mni"
    }

    selected_display_name = st.selectbox(
        "🌐 Choose Language",
        options=list(language_display_names.keys())
    )
    
    # Get the short code (e.g., 'ml') from the selected display name
    selected_language_code = language_display_names[selected_display_name]
    
    # Get the correct translation dictionary
    lang_content = LANGUAGE_DATA.get(selected_language_code, LANGUAGE_DATA["en"])
    
    # --- The rest of the sidebar inputs ---
    st.header(lang_content["fertilizer"])
    crop = st.selectbox("Select Crop", ["Wheat", "Rice", "Maize", "Sugarcane", "Potato", "Tomato"])
    soil = st.selectbox("Soil Type", ["Black", "Red", "Sandy", "Brown"])

    st.header(lang_content["loan"])
    age = st.number_input("Enter your age", min_value=18, max_value=80)
    holding = st.selectbox("Land holding (acres)", ["<1", "1-5", ">5"])

    st.header(lang_content["weather_alert"])
    user_city = st.text_input('Enter your city')

    st.header(lang_content["crop_calendar"])
    season = st.selectbox("Choose Season", ["Rabi", "Kharif", "Zaid"])

# --- 5. UI: MAIN PAGE ---
st.title(f"🌾 {lang_content['welcome']}")
if st.button("🔊 Read Welcome Message"):
    play_audio(lang_content["welcome"], lang_content["tts_lang"])

if 'fertilizer_rec' not in st.session_state: st.session_state.fertilizer_rec = ""
if 'loan_eligibility' not in st.session_state: st.session_state.loan_eligibility = ""
if 'calendar_info' not in st.session_state: st.session_state.calendar_info = ""

tab_rec, tab_weather, tab_calendar, tab_prices = st.tabs([
    "🌱 Recommendations & Schemes", lang_content["weather_alert"], 
    lang_content["crop_calendar"], lang_content["mandi_prices"]
])

with tab_rec:
    st.header(lang_content["fertilizer"])
    if st.sidebar.button("Get Recommendation"):
        st.session_state.fertilizer_rec = f"For {crop} in {soil} soil, use NPK 20:20:0 at 50kg/acre."

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

with tab_weather:
    st.header(lang_content["weather_alert"])
    st.write(f"Today's Date: {datetime.now().strftime('%d-%m-%Y')}")
    if user_city:
        weather, temp, humidity = get_weather_details(user_city)
        if weather:
            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature", f"{temp}°F")
            col2.metric("Condition", weather)
            col3.metric("Humidity", f"{humidity}%")
        else:
            st.error("City not found. Please check the name and try again.")
    else:
        st.info("Please enter a city in the sidebar to check the weather.")

with tab_calendar:
    st.header(lang_content["crop_calendar"])
    if st.sidebar.button("Show Calendar"):
        st.session_state.calendar_info = f"For the {season} season, recommended crops to sow are Wheat, Mustard, and Barley."

    if st.session_state.calendar_info:
        st.success(st.session_state.calendar_info)
        if st.button("🔊 Listen Calendar"):
            play_audio(st.session_state.calendar_info, lang_content["tts_lang"])

with tab_prices:
    st.header(lang_content["mandi_prices"])
    df = pd.DataFrame(list(MANDI_DATA.items()), columns=['Crop', 'Price (₹ per qtl)'])
    st.info("Displaying average prices per quintal (qtl). Prices may vary by location.")
    st.bar_chart(df.set_index('Crop'))
    with st.expander("View as a Table"):
        st.table(df)

# --- 6. FOOTER ---
st.markdown("---")
st.markdown("Made with ❤️ for Indian Farmers - **KrishiMitra 2.0**")