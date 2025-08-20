import streamlit as st
from datetime import datetime
from gtts import gTTS
import base64
import os

# ------------------ Utility Function ------------------
def play_audio(text, lang_code='en'):
    tts = gTTS(text=text, lang=lang_code)
    filename = "temp_audio.mp3"
    tts.save(filename)
    with open(filename, "rb") as audio_file:
        audio_bytes = audio_file.read()
    b64 = base64.b64encode(audio_bytes).decode()
    audio_html = f'<audio autoplay="true" controls="controls"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
    st.markdown(audio_html, unsafe_allow_html=True)
    os.remove(filename)

# ------------------ Language Data ------------------
LANGUAGE_DATA = {
    "English": {
        "welcome": "🌾 Welcome to KrishiMitra!",
        "fertilizer": "🌱 Fertilizer Recommendation",
        "loan": "🏦 Loan/Subsidy Checker",
        "weather_alert": "🌦️ Weather Alerts",
        "crop_calendar": "📅 Crop Calendar",
        "tts_lang": "en"
    },
    "Hindi": {
        "welcome": "🌾 कृषि मित्र में आपका स्वागत है!",
        "fertilizer": "🌱 उर्वरक सिफारिश",
        "loan": "🏦 ऋण/सब्सिडी जांच",
        "weather_alert": "🌦️ मौसम अलर्ट",
        "crop_calendar": "📅 फसल कैलेंडर",
        "tts_lang": "hi"
    },
    
    "Bengali": {
        "welcome": "🌾 কৃষি মিত্র-তে স্বাগতম!",
        "fertilizer": "🌱 সার সুপারিশ",
        "loan": "🏦 ঋণ/ভর্তুকি যাচাই",
        "weather_alert": "🌦️ আবহাওয়ার সতর্কবার্তা",
        "crop_calendar": "📅 ফসল ক্যালেন্ডার",
        "mandi_prices": "📊 মান্ডির দাম",
        "tts_lang": "bn"
    },

    "Odia": {
        "welcome": "🌾 କୃଷି ମିତ୍ରରେ ସ୍ଵାଗତ!",
        "fertilizer": "🌱 ସାର ସୁପାରିଶ",
        "loan": "🏦 ଋଣ/ସବସିଡି ଯାଞ୍ଚ",
        "weather_alert": "🌦️ ପାଣିପାଗ ସତର୍କତା",
        "crop_calendar": "📅 ଫସଲ କ୍ୟାଲେଣ୍ଡର",
        "mandi_prices": "📊 ମଣ୍ଡି ଦର",
        "tts_lang": "or"
    },

        "Assamese": {
        "welcome": "🌾 কৃষি মিত্ৰলৈ স্বাগতম!",
        "fertilizer": "🌱 সাৰৰ পৰামৰ্শ",
        "loan": "🏦 ঋণ/ৰাজসাহায্য পৰীক্ষক",
        "weather_alert": "🌦️ বতৰৰ সতৰ্কবাণী",
        "crop_calendar": "📅 শস্যৰ কেলেণ্ডাৰ",
        "mandi_prices": "📊 মন্দিৰ দৰ",
        "tts_lang": "as"
    },

    "Bhojpuri": {
        "welcome": "🌾 कृषिमित्र में रउआ स्वागत बा!",
        "fertilizer": "🌱 खाद सिफारिश",
        "loan": "🏦 कर्ज/सब्सिडी जांच",
        "weather_alert": "🌦️ मौसम चेतावनी",
        "crop_calendar": "📅 फसल कैलेंडर",
        "tts_lang": "hi"
    },
    "Punjabi": {
        "welcome": "🌾 ਕ੍ਰਿਸ਼ੀ ਮਿਤਰ ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ!",
        "fertilizer": "🌱 ਖਾਦ ਸਿਫਾਰਸ਼",
        "loan": "🏦 ਕਰਜ਼ਾ ਜਾਂ ਸਬਸਿਡੀ ਚੈੱਕਰ",
        "weather_alert": "🌦️ ਮੌਸਮ ਚੇਤਾਵਨੀ",
        "crop_calendar": "📅 ਫਸਲ ਕੈਲੰਡਰ",
        "tts_lang": "pa"
    },
    "Tamil": {
        "welcome": "🌾 கிருஷிமித்ராவிற்கு வரவேற்கிறோம்!",
        "fertilizer": "🌱 உர பரிந்துரை",
        "loan": "🏦 கடன்/தொகை சரிபார்ப்பு",
        "weather_alert": "🌦️ வானிலை எச்சரிக்கை",
        "crop_calendar": "📅 பயிர் நாட்காட்டி",
        "tts_lang": "ta"
    },
    "Telugu": {
        "welcome": "🌾 కృషిమిత్రా కు స్వాగతం!",
        "fertilizer": "🌱 ఎరువు సిఫార్సు",
        "loan": "🏦 రుణం/సబ్సిడీ తనిఖీ",
        "weather_alert": "🌦️ వాతావరణ హెచ్చరికలు",
        "crop_calendar": "📅 పంట క్యాలెండర్",
        "tts_lang": "te"
    },
    "Kannada": {
        "welcome": "🌾 ಕೃಷಿ ಮಿತ್ರಕ್ಕೆ ಸ್ವಾಗತ!",
        "fertilizer": "🌱 ರಸಗೊಬ್ಬರ ಶಿಫಾರಸು",
        "loan": "🏦 ಸಾಲ/ಸಬ್ಸಿಡಿ ತಪಾಸಣೆ",
        "weather_alert": "🌦️ ಹವಾಮಾನ ಎಚ್ಚರಿಕೆ",
        "crop_calendar": "📅 ಬೆಳೆ ದಿನದರ್ಶಿ",
        "tts_lang": "kn"
    },
    "Awadhi": {
        "welcome": "🌾 कृषिमित्र मा तोहार स्वागत बा!",
        "fertilizer": "🌱 खाद सिफारिश",
        "loan": "🏦 कर्ज/सब्सिडी जांच",
        "weather_alert": "🌦️ मौसम चेतावनी",
        "crop_calendar": "📅 फसल कैलेंडर",
        "tts_lang": "hi"
    }
}

# ------------------ Sidebar for Language ------------------
st.sidebar.title("🌐 Select Language")
language = st.sidebar.selectbox("Choose your preferred language:", list(LANGUAGE_DATA.keys()))
lang_content = LANGUAGE_DATA[language]

# ------------------ Main UI ------------------
st.title(lang_content["welcome"])

if st.button("🔊 Read Aloud"):
    play_audio(lang_content["welcome"], lang_content["tts_lang"])



# ------------------ Fertilizer Recommendation ------------------
st.header(lang_content["fertilizer"])
crop = st.selectbox("Select Crop", ["Wheat", "Rice", "Maize", "Cereals", "Sugarcane", "Potato", "Tomato"])
soil = st.selectbox("Soil Type", ["Black", "Red", "Sandy", "Brown"])
if st.button("Get Recommendation"):
    rec = f"For {crop} in {soil} soil, use NPK 20:20:0 at 50kg/acre."
    st.success(rec)
    if st.button("🔊 Listen Recommendation"):
        play_audio(rec, lang_content["tts_lang"])

# ------------------ Loan/Subsidy Checker ------------------
st.header(lang_content["loan"])
age = st.number_input("Enter your age", min_value=18, max_value=80)
holding = st.selectbox("Land holding (acres)", ["<1", "1-5", ">5"])
if st.button("Check Eligibility"):
    eligible = "You are eligible for KCC and PM-KISAN schemes."
    st.info(eligible)
    if st.button("🔊 Listen Eligibility"):
        play_audio(eligible, lang_content["tts_lang"])

# ------------------ Weather Alerts ------------------
st.header(lang_content["weather_alert"])
today = datetime.now().strftime("%d-%m-%Y")
st.write(f"Today's Date: {today}")
st.warning("⚠️ Heavy Rain Expected in your region today.")

# ------------------ Crop Calendar ------------------
st.header(lang_content["crop_calendar"])
season = st.selectbox("Choose Season", ["Rabi", "Kharif", "Zaid"])
if st.button("Show Calendar"):
    calendar = f"For {season}, sow Wheat, Mustard, and Barley."
    st.success(calendar)
    if st.button("🔊 Listen Calendar"):
        play_audio(calendar, lang_content["tts_lang"])



# ------------------ Mandi Prices ------------------
st.subheader(['price_info'])
mandi_data ={
    "wheat": "₹2200/qtl",
    "rice": "₹1800/qtl",
    "mustard": "₹5500/qtl",
    "maize": "₹1700/qtl",
    "barley": "₹1600/qtl",
    "soybean": "₹4800/qtl",
    "cotton": "₹6600/qtl",
    "groundnut": "₹5500/qtl",
    "sugarcane": "₹340/qtl",
    "potato": "₹1200/qtl",
    "onion": "₹900/qtl",
    "tomato": "₹1100/qtl",
    "bajra": "₹2150/qtl",
    "jowar": "₹2738/qtl",
    "urad dal": "₹6600/qtl",
    "moong dal": "₹7275/qtl",
    "chana": "₹5400/qtl",
    "masoor dal": "₹6000/qtl",
    "banana": "₹1500/qtl",
    "apple": "₹3000/qtl",
    "brinjal": "₹900/qtl",
    "carrot": "₹1100/qtl",
    "cabbage": "₹850/qtl",
    "peas": "₹1400/qtl"

}
st.table(mandi_data)
# ------------------ Footer ------------------
st.markdown("---")
st.markdown("Made with ❤️ for Indian Farmers - KrishiMitra")


