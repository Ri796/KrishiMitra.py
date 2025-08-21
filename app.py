import streamlit as st
import requests
import pandas as pd
from io import BytesIO

# --- 1. PAGE CONFIGURATION (Must be the FIRST Streamlit command) ---
st.set_page_config(
    page_title="KrishiMitra - AI Farming Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. BACKEND API URL ---
BACKEND_URL = "http://127.0.0.1:8000"

# --- 3. BHASHABUDDY: COMPLETE TRANSLATION DICTIONARY ---
# This version includes ALL necessary keys for ALL languages to prevent KeyErrors.
translations = {
    "en": {
        "header": "KrishiMitra", "subheader": "Your AI-powered assistant for smart farming decisions in India.",
        "bhashabuddy_header": "BhashaBuddy", "choose_language": "Choose Language:", "sidebar_info": "Select a language for a fully translated experience.",
        "tab_expert_diagnosis": "👩‍⚕️ Expert Diagnosis", "tab_mandi": "📈 Mandi Prices", "tab_health": "🌿 Crop Health", "tab_schemes": "📜 Govt. Schemes", "tab_recommendations": "🌍 Crop Recommendations",
        "expert_header": "🧠 Expert Diagnosis & Productivity Plan", "expert_desc": "Describe your crop's situation to get a detailed action plan from our AI agronomist.",
        "enter_crop": "1. Enter Your Crop:", "crop_stage": "2. Select Crop Stage:", "problem_desc": "3. Describe the Problem (e.g., 'yellow spots on lower leaves'):",
        "goal": "4. What is your primary goal?", "get_plan_button": "Generate Expert Plan", "ai_spinner": "🤖 KrishiNet AI is analyzing your situation...",
        "expert_plan_header": "Your Custom Action Plan:", "listen_plan": "Listen to this Plan", "audio_spinner": "Generating audio...", "audio_error": "Sorry, could not generate audio.",
        "chatbot_header": "💬 Quick Chat", "chat_input_placeholder": "Ask a quick question...",
        "mandi_header": "Live Mandi Prices", "mandi_desc": "Select your state and commodity to see the latest prices.", "select_state": "Select State:", "select_commodity": "Select Commodity:", "get_prices_button": "Get Prices",
        "price_spinner": "Fetching live prices...", "disease_header": "🌿 Plant Disease Detection", "disease_desc": "Upload an image of a plant leaf to detect diseases.", "upload_image": "Upload an Image:",
        "detect_disease_button": "Detect Disease", "disease_spinner": "Analyzing image...",
        "schemes_header": "📜 Government Schemes Finder", "schemes_desc": "Tell us about yourself to find relevant government schemes.", "enter_gender": "Your Gender:", "land_holding": "Land Holding (in acres):",
        "are_you_loanee": "Have you taken a loan before?", "find_schemes_button": "Find Schemes", "schemes_spinner": "Finding relevant schemes...",
        "recommendations_header": "🌍 Crop Recommendations", "recommendations_desc": "Enter your location to get crop recommendations suitable for your region.", "enter_city": "Enter Your City:",
        "enter_state": "Enter Your State:", "get_recommendations_button": "Get Recommendations", "recommendations_spinner": "Analyzing location..."
    },
    "hi": {
        "header": "कृषि मित्र", "subheader": "भारत में स्मार्ट खेती के फैसलों के लिए आपका एआई-संचालित सहायक।",
        "bhashabuddy_header": "भाषाबडी", "choose_language": "भाषा चुनें:", "sidebar_info": "पूरी तरह से अनुवादित अनुभव के लिए एक भाषा चुनें।",
        "tab_expert_diagnosis": "👩‍⚕️ विशेषज्ञ निदान", "tab_mandi": "📈 मंडी कीमतें", "tab_health": "🌿 फसल स्वास्थ्य", "tab_schemes": "📜 सरकारी योजनाएं", "tab_recommendations": "🌍 फसल सिफारिशें",
        "expert_header": "🧠 विशेषज्ञ निदान और उत्पादकता योजना", "expert_desc": "हमारे एआई कृषि विज्ञानी से विस्तृत कार्य योजना प्राप्त करने के लिए अपनी फसल की स्थिति का वर्णन करें।",
        "enter_crop": "1. अपनी फसल दर्ज करें:", "crop_stage": "2. फसल की अवस्था चुनें:", "problem_desc": "3. समस्या का वर्णन करें (जैसे, 'निचली पत्तियों पर पीले धब्बे'):", "goal": "4. आपका प्राथमिक लक्ष्य क्या है?", "get_plan_button": "विशेषज्ञ योजना बनाएं", "ai_spinner": "🤖 कृषिनेत्र एआई आपकी स्थिति का विश्लेषण कर रहा है...", "expert_plan_header": "आपकी कस्टम कार्य योजना:", "listen_plan": "इस योजना को सुनें", "audio_spinner": "ऑडियो बना रहा है...", "audio_error": "क्षमा करें, ऑडियो नहीं बन सका।",
        "chatbot_header": "💬 त्वरित चैट", "chat_input_placeholder": "एक त्वरित प्रश्न पूछें...",
        "mandi_header": "लाइव मंडी कीमतें", "mandi_desc": "नवीनतम कीमतें देखने के लिए अपना राज्य और वस्तु चुनें।", "select_state": "राज्य चुनें:", "select_commodity": "वस्तु चुनें:", "get_prices_button": "कीमतें प्राप्त करें", "price_spinner": "लाइव कीमतें प्राप्त हो रही हैं...",
        "disease_header": "🌿 पौधे की बीमारी का पता लगाना", "disease_desc": "बीमारियों का पता लगाने के लिए पौधे की पत्ती की एक छवि अपलोड करें।", "upload_image": "एक छवि अपलोड करें:", "detect_disease_button": "बीमारी का पता लगाएं", "disease_spinner": "छवि का विश्लेषण हो रहा है...",
        "schemes_header": "📜 सरकारी योजना खोजक", "schemes_desc": "प्रासंगिक सरकारी योजनाओं को खोजने के लिए हमें अपने बारे में बताएं।", "enter_gender": "आपका लिंग:", "land_holding": "भूमि धारण (एकड़ में):", "are_you_loanee": "क्या आपने पहले ऋण लिया है?", "find_schemes_button": "योजनाएं खोजें", "schemes_spinner": "प्रासंगिक योजनाएं खोजी जा रही हैं...",
        "recommendations_header": "🌍 फसल सिफारिशें", "recommendations_desc": "अपने क्षेत्र के लिए उपयुक्त फसल सिफारिशें प्राप्त करने के लिए अपना स्थान दर्ज करें।", "enter_city": "अपना शहर दर्ज करें:", "enter_state": "अपना राज्य दर्ज करें:", "get_recommendations_button": "सिफारिशें प्राप्त करें", "recommendations_spinner": "स्थान का विश्लेषण हो रहा है..."
    },
    "mr": {
        "header": "कृषीमित्र", "subheader": "भारतातील स्मार्ट शेतीच्या निर्णयांसाठी तुमचा एआय-शक्ती असलेला सहाय्यक।", "bhashabuddy_header": "भाषाबडी", "choose_language": "भाषा निवडा:", "sidebar_info": "पूर्णपणे अनुवादित अनुभवासाठी एक भाषा निवडा।",
        "tab_expert_diagnosis": "👩‍⚕️ विशेषज्ञ निदान", "tab_mandi": "📈 मंडी भाव", "tab_health": "🌿 पीक आरोग्य", "tab_schemes": "📜 सरकारी योजना", "tab_recommendations": "🌍 पीक शिफारसी",
        "expert_header": "🧠 विशेषज्ञ निदान आणि उत्पादकता योजना", "expert_desc": "आमच्या एआय कृषीशास्त्रज्ञाकडून तपशीलवार कृती योजना मिळवण्यासाठी तुमच्या पिकाची परिस्थिती सांगा।",
        "enter_crop": "१. तुमचे पीक प्रविष्ट करा:", "crop_stage": "२. पिकाचा टप्पा निवडा:", "problem_desc": "३. समस्येचे वर्णन करा (उदा. 'खालच्या पानांवर पिवळे डाग'):", "goal": "४. तुमचे प्राथमिक ध्येय काय आहे?", "get_plan_button": "विशेषज्ञ योजना तयार करा",
        "ai_spinner": "🤖 कृषीनेट एआय तुमच्या परिस्थितीचे विश्लेषण करत आहे...", "expert_plan_header": "तुमची सानुकूल कृती योजना:", "listen_plan": "ही योजना ऐका", "audio_spinner": "ऑडिओ तयार होत आहे...", "audio_error": "क्षमस्व, ऑडिओ तयार करता आला नाही।",
        "chatbot_header": "💬 त्वरित गप्पा", "chat_input_placeholder": "एक त्वरित प्रश्न विचारा...", "mandi_header": "लाइव्ह मंडी भाव", "mandi_desc": "नवीनतम भाव पाहण्यासाठी तुमचे राज्य आणि कमोडिटी निवडा।", "select_state": "राज्य निवडा:", "select_commodity": "कमोडिटी निवडा:",
        "get_prices_button": "भाव मिळवा", "price_spinner": "लाइव्ह भाव मिळवत आहे...", "disease_header": "🌿 पीक रोग निदान", "disease_desc": "रोगांचे निदान करण्यासाठी वनस्पतीच्या पानाचा फोटो अपलोड करा।", "upload_image": "फोटो अपलोड करा:", "detect_disease_button": "रोगाचे निदान करा",
        "disease_spinner": "फोटोचे विश्लेषण करत आहे...", "schemes_header": "📜 सरकारी योजना शोधक", "schemes_desc": "संबंधित सरकारी योजना शोधण्यासाठी आम्हाला तुमच्याबद्दल सांगा।", "enter_gender": "तुमचे लिंग:", "land_holding": "जमीन धारणा (एकर मध्ये):",
        "are_you_loanee": "तुम्ही आधी कर्ज घेतले आहे का?", "find_schemes_button": "योजना शोधा", "schemes_spinner": "संबंधित योजना शोधत आहे...", "recommendations_header": "🌍 पीक शिफारसी", "recommendations_desc": "तुमच्या प्रदेशासाठी योग्य पीक शिफारसी मिळवण्यासाठी तुमचे स्थान प्रविष्ट करा।",
        "enter_city": "तुमचे शहर प्रविष्ट करा:", "enter_state": "तुमचे राज्य प्रविष्ट करा:", "get_recommendations_button": "शिफारसी मिळवा", "recommendations_spinner": "स्थानाचे विश्लेषण करत आहे..."
    },

    "gu": {
        "header": "કૃષિમિત્ર", "subheader": "ભારતમાં સ્માર્ટ ખેતીના નિર્ણયો માટે તમારા એઆઈ-સંચાલિત સહાયક।", "bhashabuddy_header": "ભાષાબડી", "choose_language": "ભાષા પસંદ કરો:", "sidebar_info": "સંપૂર્ણ અનુવાદિત અનુભવ માટે ભાષા પસંદ કરો।",
        "tab_expert_diagnosis": "👩‍⚕️ નિષ્ણાત નિદાન", "tab_mandi": "📈 મંડીના ભાવ", "tab_health": "🌿 પાકનું આરોગ્ય", "tab_schemes": "📜 સરકારી યોજનાઓ", "tab_recommendations": "🌍 પાકની ભલામણો",
        "expert_header": "🧠 નિષ્ણાત નિદાન અને ઉત્પાદકતા યોજના", "expert_desc": "અમારા એઆઈ કૃષિવિજ્ઞાની પાસેથી વિગતવાર કાર્ય યોજના મેળવવા માટે તમારા પાકની પરિસ્થિતિનું વર્ણન કરો।",
        "enter_crop": "૧. તમારો પાક દાખલ કરો:", "crop_stage": "૨. પાકનો તબક્કો પસંદ કરો:", "problem_desc": "૩. સમસ્યાનું વર્ણન કરો (દા.ત., 'નીચલા પાંદડા પર પીળા ડાઘ'):", "goal": "૪. તમારું પ્રાથમિક લક્ષ્ય શું છે?", "get_plan_button": "નિષ્ણાત યોજના બનાવો",
        "ai_spinner": "🤖 કૃષિનેટ એઆઈ તમારી પરિસ્થિતિનું વિશ્લેષણ કરી રહ્યું છે...", "expert_plan_header": "તમારી કસ્ટમ કાર્ય યોજના:", "listen_plan": "આ યોજના સાંભળો", "audio_spinner": "ઓડિયો જનરેટ કરી રહ્યું છે...", "audio_error": "માફ કરશો, ઓડિયો જનરેટ કરી શકાયો નથી।",
        "chatbot_header": "💬 ઝડપી ચેટ", "chat_input_placeholder": "એક ઝડપી પ્રશ્ન પૂછો...", "mandi_header": "લાઇવ મંડીના ભાવ", "mandi_desc": "નવીનતમ ભાવો જોવા માટે તમારું રાજ્ય અને કોમોડિટી પસંદ કરો।", "select_state": "રાજ્ય પસંદ કરો:", "select_commodity": "કોમોડિટી પસંદ કરો:",
        "get_prices_button": "ભાવો મેળવો", "price_spinner": "લાઇવ ભાવ મેળવી રહ્યું છે...", "disease_header": "🌿 વનસ્પતિ રોગની શોધ", "disease_desc": "રોગો શોધવા માટે વનસ્પતિના પાનનો ફોટો અપલોડ કરો।", "upload_image": "ફોટો અપલોડ કરો:", "detect_disease_button": "રોગ શોધો",
        "disease_spinner": "ફોટોનું વિશ્લેષણ કરી રહ્યું છે...", "schemes_header": "📜 સરકારી યોજનાઓ શોધક", "schemes_desc": "સંબંધિત સરકારી યોજનાઓ શોધવા માટે અમને તમારા વિશે કહો।", "enter_gender": "તમારું લિંગ:", "land_holding": "જમીન ધારણ (એકરમાં):",
        "are_you_loanee": "શું તમે પહેલાં લોન લીધી છે?", "find_schemes_button": "યોજનાઓ શોધો", "schemes_spinner": "સંબંધિત યોજનાઓ શોધી રહ્યું છે...", "recommendations_header": "🌍 પાકની ભલામણો", "recommendations_desc": "તમારા પ્રદેશ માટે યોગ્ય પાકની ભલામણો મેળવવા માટે તમારું સ્થાન દાખલ કરો।",
        "enter_city": "તમારું શહેર દાખલ કરો:", "enter_state": "તમારું રાજ્ય દાખલ કરો:", "get_recommendations_button": "ભલામણો મેળવો", "recommendations_spinner": "સ્થાનનું વિશ્લેષણ કરી રહ્યું છે..."
    },
    
    "bn": {
    "header": "কৃষিমিত্র",
    "subheader": "ভারতে স্মার্ট কৃষি সিদ্ধান্তের জন্য আপনার এআই-চালিত সহকারী।",
    "bhashabuddy_header": "ভাষাসাথী",
    "choose_language": "ভাষা নির্বাচন করুন:",
    "sidebar_info": "একটি সম্পূর্ণ অনূদিত অভিজ্ঞতার জন্য একটি ভাষা নির্বাচন করুন।",
    "tab_expert_diagnosis": "👩‍⚕️ বিশেষজ্ঞ নির্ণয়",
    "tab_mandi": "📈 মন্ডি দর",
    "tab_health": "🌿 ফসল স্বাস্থ্য",
    "tab_schemes": "📜 সরকারি প্রকল্প",
    "tab_recommendations": "🌍 ফসল সুপারিশ",
    "expert_header": "🧠 বিশেষজ্ঞ নির্ণয় ও উৎপাদনশীলতা পরিকল্পনা",
    "expert_desc": "আমাদের এআই কৃষিবিদের কাছ থেকে একটি বিস্তারিত কর্ম পরিকল্পনা পেতে আপনার ফসলের পরিস্থিতি বর্ণনা করুন।",
    "enter_crop": "১. আপনার ফসল লিখুন:",
    "crop_stage": "২. ফসলের পর্যায় নির্বাচন করুন:",
    "problem_desc": "৩. সমস্যা বর্ণনা করুন (যেমন, 'নিচের পাতায় হলুদ দাগ'):",
    "goal": "৪. আপনার প্রাথমিক লক্ষ্য কি?",
    "get_plan_button": "বিশেষজ্ঞ পরিকল্পনা তৈরি করুন",
    "ai_spinner": "🤖 কৃষিনেট এআই আপনার পরিস্থিতি বিশ্লেষণ করছে...",
    "expert_plan_header": "আপনার কাস্টম কর্ম পরিকল্পনা:",
    "listen_plan": "এই পরিকল্পনাটি শুনুন",
    "audio_spinner": "অডিও তৈরি হচ্ছে...",
    "audio_error": "দুঃখিত, অডিও তৈরি করা যায়নি।",
    "chatbot_header": "💬 দ্রুত চ্যাট",
    "chat_input_placeholder": "একটি দ্রুত প্রশ্ন জিজ্ঞাসা করুন...",
    },

    "as": {
        "header": "কৃষি মিত্ৰ", "subheader": "ভাৰতত স্মাৰ্ট কৃষি সিদ্ধান্তৰ বাবে আপোনাৰ AI-চালিত সহায়ক।",
        "bhashabuddy_header": "ভাষা বন্ধু", "choose_language": "ভাষা নিৰ্বাচন কৰক:", "sidebar_info": "সম্পূৰ্ণ অনুবাদিত অভিজ্ঞতাৰ বাবে এটা ভাষা নিৰ্বাচন কৰক।",
        "tab_expert_diagnosis": "👩‍⚕️ বিশেষজ্ঞ নিদান", "tab_mandi": "📈 মন্দিৰ দৰ", "tab_health": "🌿 শস্যৰ স্বাস্থ্য", "tab_schemes": "📜 চৰকাৰী আঁচনি", "tab_recommendations": "🌍 শস্যৰ চুপাৰিছ",
        "expert_header": "🧠 বিশেষজ্ঞ নিদান আৰু उत्पादकता পৰিকল্পনা", "expert_desc": "আমাৰ AI কৃষি বিজ্ঞানীৰ পৰা বিতং কাৰ্য পৰিকল্পনা পাবলৈ আপোনাৰ শস্যৰ অৱস্থা বৰ্ণনা কৰক।",
        "enter_crop": "১. আপোনাৰ শস্য দিয়ক:", "crop_stage": "২. শস্যৰ স্তৰ নিৰ্বাচন কৰক:", "problem_desc": "৩. সমস্যা বৰ্ণনা কৰক (যেনে, 'তলৰ পাতত হালধীয়া দাগ'):",
        "goal": "৪. আপোনাৰ প্ৰাথমিক লক্ষ্য কি?", "get_plan_button": "বিশেষজ্ঞ পৰিকল্পনা সৃষ্টি কৰক", "ai_spinner": "🤖 কৃষি নেট AI আপোনাৰ অৱস্থা বিশ্লেষণ কৰি আছে...",
        "expert_plan_header": "আপোনাৰ কাষ্টম কাৰ্য পৰিকল্পনা:", "listen_plan": "এই পৰিকল্পনা শুনক", "audio_spinner": "অডিঅ' সৃষ্টি হৈ আছে...", "audio_error": "দুঃখিত, অডিঅ' সৃষ্টি কৰিব পৰা নগল।",
        "chatbot_header": "💬 খৰতকীয়া চাট", "chat_input_placeholder": "এটা খৰতকীয়া প্ৰশ্ন সোধক...",
        "mandi_header": "লাইভ মন্দিৰ দৰ", "mandi_desc": "শেহতীয়া দৰ চাবলৈ আপোনাৰ ৰাজ্য আৰু সামগ্ৰী নিৰ্বাচন কৰক।", "select_state": "ৰাজ্য নিৰ্বাচন কৰক:", "select_commodity": "সামগ্ৰী নিৰ্বাচন কৰক:", "get_prices_button": "দৰ পাওক",
        "price_spinner": "লাইভ দৰ সংগ্ৰহ কৰি আছে...", "disease_header": "🌿 উদ্ভিদৰ ৰোগ চিনাক্তকৰণ", "disease_desc": "ৰোগ চিনাক্ত কৰিবলৈ উদ্ভিদৰ পাতৰ এখন ছবি আপলোড কৰক।", "upload_image": "এখন ছবি আপলোড কৰক:",
        "detect_disease_button": "ৰোগ চিনাক্ত কৰক", "disease_spinner": "ছবি বিশ্লেষণ কৰি আছে...",
        "schemes_header": "📜 চৰকাৰী আঁচনি সন্ধানকাৰী", "schemes_desc": "প্ৰাসংগিক চৰকাৰী আঁচনি বিচাৰিবলৈ আপোনাৰ বিষয়ে কওক।", "enter_gender": "আপোনাৰ লিংগ:", "land_holding": "মাটিৰ পৰিমাণ (একৰত):",
        "are_you_loanee": "আপুনি আগতে ঋণ লৈছে নেকি?", "find_schemes_button": "আঁচনি বিচাৰক", "schemes_spinner": "প্ৰাসংগিক আঁচনি বিচাৰি আছে...",
        "recommendations_header": "🌍 শস্যৰ চুপাৰিছ", "recommendations_desc": "আপোনাৰ অঞ্চলৰ বাবে উপযুক্ত শস্যৰ চুপাৰিছ পাবলৈ আপোনাৰ অৱস্থান দিয়ক।", "enter_city": "আপোনাৰ চহৰ দিয়ক:",
        "enter_state": "আপোনাৰ ৰাজ্য দিয়ক:", "get_recommendations_button": "চুপাৰিছ পাওক", "recommendations_spinner": "অৱস্থান বিশ্লেষণ কৰি আছে..."
    },

    "or": {
        "header": "କୃଷି ମିତ୍ର", "subheader": "ଭାରତରେ ସ୍ମାର୍ଟ କୃଷି ନିଷ୍ପତ୍ତି ପାଇଁ ଆପଣଙ୍କ AI-ଚାଳିତ ସହାୟକ।",
        "bhashabuddy_header": "ଭାଷା ବନ୍ଧୁ", "choose_language": "ଭାଷା ବାଛନ୍ତୁ:", "sidebar_info": "ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଅନୁବାଦିତ ଅନୁଭୂତି ପାଇଁ ଏକ ଭାଷା ବାଛନ୍ତୁ।",
        "tab_expert_diagnosis": "👩‍⚕️ ବିଶେଷଜ୍ଞ ନିଦାନ", "tab_mandi": "📈 ମଣ୍ଡି ଦର", "tab_health": "🌿 ଫସଲ ସ୍ୱାସ୍ଥ୍ୟ", "tab_schemes": "📜 ସରକାରୀ ଯୋଜନା", "tab_recommendations": "🌍 ଫସଲ ସୁପାରିଶ",
        "expert_header": "🧠 ବିଶେଷଜ୍ଞ ନିଦାନ ଏବଂ ଉତ୍ପାଦକତା ଯୋଜନା", "expert_desc": "ଆମର AI କୃଷି ବିଜ୍ଞାନୀଙ୍କଠାରୁ ଏକ ବିସ୍ତୃତ କାର୍ଯ୍ୟ ଯୋଜନା ପାଇବାକୁ ଆପଣଙ୍କ ଫସଲର ସ୍ଥିତି ବର୍ଣ୍ଣନା କରନ୍ତୁ।",
        "enter_crop": "୧. ଆପଣଙ୍କ ଫସଲ ଦିଅନ୍ତୁ:", "crop_stage": "୨. ଫସଲର ପର୍ଯ୍ୟାୟ ବାଛନ୍ତୁ:", "problem_desc": "୩. ସମସ୍ୟା ବର୍ଣ୍ଣନା କରନ୍ତୁ (ଯେପରି, 'ତଳ ପତ୍ରରେ ହଳଦିଆ ଦାଗ'):",
        "goal": "୪. ଆପଣଙ୍କର ପ୍ରାଥମିକ ଲକ୍ଷ୍ୟ କ'ଣ?", "get_plan_button": "ବିଶେଷଜ୍ଞ ଯୋଜନା ପ୍ରସ୍ତୁତ କରନ୍ତୁ", "ai_spinner": "🤖 କୃଷି ନେଟ୍ AI ଆପଣଙ୍କ ସ୍ଥିତି ବିଶ୍ଳେଷଣ କରୁଛି...",
        "expert_plan_header": "ଆପଣଙ୍କ କଷ୍ଟମ୍ କାର୍ଯ୍ୟ ଯୋଜନା:", "listen_plan": "ଏହି ଯୋଜନା ଶୁଣନ୍ତୁ", "audio_spinner": "ଅଡିଓ ପ୍ରସ୍ତୁତ ହେଉଛି...", "audio_error": "କ୍ଷମା କରନ୍ତୁ, ଅଡିଓ ପ୍ରସ୍ତୁତ ହୋଇପାରିଲା ନାହିଁ।",
        "chatbot_header": "💬 ତୁରନ୍ତ ଚାଟ୍", "chat_input_placeholder": "ଏକ ତୁରନ୍ତ ପ୍ରଶ୍ନ ପଚାରନ୍ତୁ...",
        "mandi_header": "ଲାଇଭ ମଣ୍ଡି ଦର", "mandi_desc": "ନୂତନ ଦର ଦେଖିବା ପାଇଁ ଆପଣଙ୍କ ରାଜ୍ୟ ଏବଂ ସାମଗ୍ରୀ ବାଛନ୍ତୁ।", "select_state": "ରାଜ୍ୟ ବାଛନ୍ତୁ:", "select_commodity": "ସାମଗ୍ରୀ ବାଛନ୍ତୁ:", "get_prices_button": "ଦର ପାଆନ୍ତୁ",
        "price_spinner": "ଲାଇଭ ଦର ଅଣାଯାଉଛି...", "disease_header": "🌿 ଉଦ୍ଭିଦ ରୋଗ ଚିହ୍ନଟ", "disease_desc": "ରୋଗ ଚିହ୍ନଟ କରିବାକୁ ଉଦ୍ଭିଦର ପତ୍ରର ଏକ ଛବି ଅପଲୋଡ୍ କରନ୍ତୁ।", "upload_image": "ଏକ ଛବି ଅପଲୋଡ୍ କରନ୍ତୁ:",
        "detect_disease_button": "ରୋଗ ଚିହ୍ନଟ କରନ୍ତୁ", "disease_spinner": "ଛବି ବିଶ୍ଳେଷଣ କରାଯାଉଛି...",
        "schemes_header": "📜 ସରକାରୀ ଯୋଜନା ଖୋଜକ", "schemes_desc": "ପ୍ରାସଙ୍ଗିକ ସରକାରୀ ଯୋଜନା ଖୋଜିବା ପାଇଁ ଆମକୁ ଆପଣଙ୍କ ବିଷୟରେ କୁହନ୍ତୁ।", "enter_gender": "ଆପଣଙ୍କ ଲିଙ୍ଗ:", "land_holding": "ଜମି ପରିମାଣ (ଏକରରେ):",
        "are_you_loanee": "ଆପଣ ପୂର୍ବରୁ ଋଣ ନେଇଛନ୍ତି କି?", "find_schemes_button": "ଯୋଜନା ଖୋଜନ୍ତୁ", "schemes_spinner": "ପ୍ରାସଙ୍ଗିକ ଯୋଜନା ଖୋଜାଯାଉଛି...",
        "recommendations_header": "🌍 ଫସଲ ସୁପାରିଶ", "recommendations_desc": "ଆପଣଙ୍କ ଅଞ୍ଚଳ ପାଇଁ ଉପଯୁକ୍ତ ଫସଲ ସୁପାରିଶ ପାଇବାକୁ ଆପଣଙ୍କ ସ୍ଥାନ ଦିଅନ୍ତୁ।", "enter_city": "ଆପଣଙ୍କ ସହର ଦିଅନ୍ତୁ:",
        "enter_state": "ଆପଣଙ୍କ ରାଜ୍ୟ ଦିଅନ୍ତୁ:", "get_recommendations_button": "ସୁପାରିଶ ପାଆନ୍ତୁ", "recommendations_spinner": "ସ୍ଥାନ ବିଶ୍ଳେଷଣ କରାଯାଉଛି..."
    },

    "ta": {
    "header": "கிருஷிமித்ரா",
    "subheader": "இந்தியாவில் ஸ்மார்ட் விவசாய முடிவுகளுக்கு உங்கள் AI-இயங்கும் உதவியாளர்.",
    "bhashabuddy_header": "பாஷாபட்டி",
    "choose_language": "மொழியைத் தேர்ந்தெடுக்கவும்:",
    "sidebar_info": "முழுமையாக மொழிபெயர்க்கப்பட்ட அனுபவத்திற்கு ஒரு மொழியைத் தேர்ந்தெடுக்கவும்.",
    "tab_expert_diagnosis": "👩‍⚕️ நிபுணர் கண்டறிதல்",
    "tab_mandi": "📈 மண்டி விலைகள்",
    "tab_health": "🌿 பயிர் ஆரோக்கியம்",
    "tab_schemes": "📜 அரசாங்க திட்டங்கள்",
    "tab_recommendations": "🌍 பயிர் பரிந்துரைகள்",
    "expert_header": "🧠 நிபுணர் கண்டறிதல் மற்றும் உற்பத்தித்திறன் திட்டம்",
    "expert_desc": "எங்கள் AI விவசாய விஞ்ஞானியிடமிருந்து விரிவான செயல் திட்டத்தைப் பெற உங்கள் பயிர் நிலையை விவரிக்கவும்.",
    "enter_crop": "1. உங்கள் பயிரை உள்ளிடவும்:",
    "crop_stage": "2. பயிர் நிலையைத் தேர்ந்தெடுக்கவும்:",
    "problem_desc": "3. சிக்கலை விவரிக்கவும் (எ.கா., 'கீழ் இலைகளில் மஞ்சள் புள்ளிகள்'):",
    "goal": "4. உங்கள் முதன்மை இலக்கு என்ன?",
    "get_plan_button": "நிபுணர் திட்டத்தை உருவாக்கவும்",
    "ai_spinner": "🤖 கிருஷிநெட் AI உங்கள் நிலையை பகுப்பாய்வு செய்கிறது...",
    "expert_plan_header": "உங்கள் தனிப்பயன் செயல் திட்டம்:",
    "listen_plan": "இந்தத் திட்டத்தைக் கேட்கவும்",
    "audio_spinner": "ஆடியோ உருவாக்கப்படுகிறது...",
    "audio_error": "மன்னிக்கவும், ஆடியோவை உருவாக்க முடியவில்லை.",
    "chatbot_header": "💬 விரைவான அரட்டை",
    "chat_input_placeholder": "ஒரு விரைவான கேள்வியைக் கேட்கவும்...",
    },
    "te": {
    "header": "కృషిమిత్ర",
    "subheader": "భారతదేశంలో స్మార్ట్ వ్యవసాయ నిర్ణయాల కోసం మీ AI-ఆధారిత సహాయకుడు.",
    "bhashabuddy_header": "భాషాబడ్డీ",
    "choose_language": "భాషను ఎంచుకోండి:",
    "sidebar_info": "పూర్తిగా అనువదించబడిన అనుభవం కోసం ఒక భాషను ఎంచుకోండి.",
    "tab_expert_diagnosis": "👩‍⚕️ నిపుణుల నిర్ధారణ",
    "tab_mandi": "📈 మండి ధరలు",
    "tab_health": "🌿 పంట ఆరోగ్యం",
    "tab_schemes": "📜 ప్రభుత్వ పథకాలు",
    "tab_recommendations": "🌍 పంట సిఫార్సులు",
    "expert_header": "🧠 నిపుణుల నిర్ధారణ మరియు ఉత్పాదకత ప్రణాళిక",
    "expert_desc": "మా AI వ్యవసాయ శాస్త్రవేత్త నుండి వివరణాత్మక కార్యాచరణ ప్రణాళికను పొందడానికి మీ పంట పరిస్థితిని వివరించండి.",
    "enter_crop": "1. మీ పంటను నమోదు చేయండి:",
    "crop_stage": "2. పంట దశను ఎంచుకోండి:",
    "problem_desc": "3. సమస్యను వివరించండి (ఉదా., 'దిగువ ఆకులపై పసుపు మచ్చలు'):",
    "goal": "4. మీ ప్రాథమిక లక్ష్యం ఏమిటి?",
    "get_plan_button": "నిపుణుల ప్రణాళికను రూపొందించండి",
    "ai_spinner": "🤖 కృషిநெட் AI మీ పరిస్థితిని విశ్లేషిస్తోంది...",
    "expert_plan_header": "మీ కస్టమ్ కార్యాచరణ ప్రణాళిక:",
    "listen_plan": "ఈ ప్రణాళికను వినండి",
    "audio_spinner": "ఆడియో సృష్టించబడుతోంది...",
    "audio_error": "క్షమించండి, ఆడియోను సృష్టించడం సాధ్యం కాలేదు.",
    "chatbot_header": "💬 త్వరిత చాట్",
    "chat_input_placeholder": "ఒక శీఘ్ర ప్రశ్న అడగండి...",
    },
    "kn": {
    "header": "ಕೃಷಿಮಿತ್ರ",
    "subheader": "ಭಾರತದಲ್ಲಿ ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ನಿರ್ಧಾರಗಳಿಗಾಗಿ ನಿಮ್ಮ AI-ಚಾಲಿತ ಸಹಾಯಕ.",
    "bhashabuddy_header": "ಭಾಷಾಬಡ್ಡಿ",
    "choose_language": "ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
    "sidebar_info": "ಸಂಪೂರ್ಣ ಅನುವಾದಿತ ಅನುಭವಕ್ಕಾಗಿ ಒಂದು ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
    "tab_expert_diagnosis": "👩‍⚕️ ತಜ್ಞರ ರೋಗನಿರ್ಣಯ",
    "tab_mandi": "📈 ಮಂಡಿ ಬೆಲೆಗಳು",
    "tab_health": "🌿 ಬೆಳೆ ಆರೋಗ್ಯ",
    "tab_schemes": "📜 ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು",
    "tab_recommendations": "🌍 ಬೆಳೆ ಶಿಫಾರಸುಗಳು",
    "expert_header": "🧠 ತಜ್ಞರ ರೋಗನಿರ್ಣಯ ಮತ್ತು ಉತ್ಪಾದಕತೆ ಯೋಜನೆ",
    "expert_desc": "ನಮ್ಮ AI ಕೃಷಿ ವಿಜ್ಞಾನಿಯಿಂದ ವಿವರವಾದ ಕ್ರಿಯಾ ಯೋಜನೆಯನ್ನು ಪಡೆಯಲು ನಿಮ್ಮ ಬೆಳೆ ಪರಿಸ್ಥಿತಿಯನ್ನು ವಿವರಿಸಿ.",
    "enter_crop": "1. ನಿಮ್ಮ ಬೆಳೆಯನ್ನು ನಮೂದಿಸಿ:",
    "crop_stage": "2. ಬೆಳೆ ಹಂತವನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
    "problem_desc": "3. ಸಮಸ್ಯೆಯನ್ನು ವಿವರಿಸಿ (ಉದಾ., 'ಕೆಳಗಿನ ಎಲೆಗಳ ಮೇಲೆ ಹಳದಿ ಚುಕ್ಕೆಗಳು'):",
    "goal": "4. ನಿಮ್ಮ ಪ್ರಾಥಮಿಕ ಗುರಿ ಏನು?",
    "get_plan_button": "ತಜ್ಞರ ಯೋಜನೆಯನ್ನು ರಚಿಸಿ",
    "ai_spinner": "🤖 ಕೃಷಿನೆಟ್ AI ನಿಮ್ಮ ಪರಿಸ್ಥಿತಿಯನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತಿದೆ...",
    "expert_plan_header": "ನಿಮ್ಮ ಕಸ್ಟಮ್ ಕ್ರಿಯಾ ಯೋಜನೆ:",
    "listen_plan": "ಈ ಯೋಜನೆಯನ್ನು ಕೇಳಿ",
    "audio_spinner": "ಆಡಿಯೋ ರಚಿಸಲಾಗುತ್ತಿದೆ...",
    "audio_error": "ಕ್ಷಮಿಸಿ, ಆಡಿಯೋ ರಚಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ.",
    "chatbot_header": "💬 ತ್ವರಿತ ಚಾಟ್",
    "chat_input_placeholder": "ಒಂದು ತ್ವರಿತ ಪ್ರಶ್ನೆ ಕೇಳಿ...",
    },
    "pa": {
    "header": "ਕ੍ਰਿਸ਼ੀਮਿੱਤਰ",
    "subheader": "ਭਾਰਤ ਵਿੱਚ ਸਮਾਰਟ ਖੇਤੀ ਦੇ ਫੈਸਲਿਆਂ ਲਈ ਤੁਹਾਡਾ AI-ਸੰਚਾਲਿਤ ਸਹਾਇਕ।",
    "bhashabuddy_header": "ਭਾਸ਼ਾਬੱਡੀ",
    "choose_language": "ਭਾਸ਼ਾ ਚੁਣੋ:",
    "sidebar_info": "ਪੂਰੀ ਤਰ੍ਹਾਂ ਅਨੁਵਾਦ ਕੀਤੇ ਅਨੁਭਵ ਲਈ ਇੱਕ ਭਾਸ਼ਾ ਚੁਣੋ।",
    "tab_expert_diagnosis": "👩‍⚕️ ਮਾਹਰ ਨਿਦਾਨ",
    "tab_mandi": "📈 ਮੰਡੀ ਦੀਆਂ ਕੀਮਤਾਂ",
    "tab_health": "🌿 ਫਸਲ ਦੀ ਸਿਹਤ",
    "tab_schemes": "📜 ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ",
    "tab_recommendations": "🌍 ਫਸਲ ਦੀਆਂ ਸਿਫਾਰਸ਼ਾਂ",
    "expert_header": "🧠 ਮਾਹਰ ਨਿਦਾਨ ਅਤੇ ਉਤਪਾਦਕਤਾ ਯੋਜਨਾ",
    "expert_desc": "ਸਾਡੇ AI ਖੇਤੀ ਵਿਗਿਆਨੀ ਤੋਂ ਵਿਸਤ੍ਰਿਤ ਕਾਰਜ ਯੋਜਨਾ ਪ੍ਰਾਪਤ ਕਰਨ ਲਈ ਆਪਣੀ ਫਸਲ ਦੀ ਸਥਿਤੀ ਦਾ ਵਰਣਨ ਕਰੋ।",
    "enter_crop": "1. ਆਪਣੀ ਫਸਲ ਦਾਖਲ ਕਰੋ:",
    "crop_stage": "2. ਫਸਲ ਦਾ ਪੜਾਅ ਚੁਣੋ:",
    "problem_desc": "3. ਸਮੱਸਿਆ ਦਾ ਵਰਣਨ ਕਰੋ (ਜਿਵੇਂ, 'ਹੇਠਲੇ ਪੱਤਿਆਂ 'ਤੇ ਪੀਲੇ ਧੱਬੇ'):",
    "goal": "4. ਤੁਹਾਡਾ ਮੁੱਖ ਟੀਚਾ ਕੀ ਹੈ?",
    "get_plan_button": "ਮਾਹਰ ਯੋਜਨਾ ਬਣਾਓ",
    "ai_spinner": "🤖 ਕ੍ਰਿਸ਼ੀਨੈੱਟ AI ਤੁਹਾਡੀ ਸਥਿਤੀ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰ ਰਿਹਾ ਹੈ...",
    "expert_plan_header": "ਤੁਹਾਡੀ ਕਸਟਮ ਕਾਰਜ ਯੋਜਨਾ:",
    "listen_plan": "ਇਸ ਯੋਜਨਾ ਨੂੰ ਸੁਣੋ",
    "audio_spinner": "ਆਡੀਓ ਬਣਾਇਆ ਜਾ ਰਿਹਾ ਹੈ...",
    "audio_error": "ਮਾਫ ਕਰਨਾ, ਆਡੀਓ ਨਹੀਂ ਬਣਾਇਆ ਜਾ ਸਕਿਆ।",
    "chatbot_header": "� ਤੁਰੰਤ ਗੱਲਬਾਤ",
    "chat_input_placeholder": "ਇੱਕ ਤੁਰੰਤ ਸ",
    },

    "ml": {
        "header": "കൃഷി മിത്ര",
        "subheader": "ഇന്ത്യയിലെ സ്മാർട്ട് കാർഷിക തീരുമാനങ്ങൾക്കായി നിങ്ങളുടെ AI-പവർ ചെയ്യുന്ന സഹായി.",
        "bhashabuddy_header": "ഭാഷാ ബഡ്ഡി",
        "choose_language": "ഭാഷ തിരഞ്ഞെടുക്കുക:",
        "sidebar_info": "പൂർണ്ണമായി വിവർത്തനം ചെയ്ത അനുഭവത്തിനായി ഒരു ഭാഷ തിരഞ്ഞെടുക്കുക.",
        "tab_expert_diagnosis": "👩‍⚕️ വിദഗ്ദ്ധ രോഗനിർണയം",
        "tab_mandi": "📈 മണ്ഡി വിലകൾ",
        "tab_health": "🌿 വിള ആരോഗ്യം",
        "tab_schemes": "📜 സർക്കാർ പദ്ധതികൾ",
        "tab_recommendations": "🌍 വിള ശുപാർശകൾ",
        "expert_header": "🧠 വിദഗ്ദ്ധ രോഗനിർണയവും ഉത്പാദനക്ഷമതാ പദ്ധതിയും",
        "expert_desc": "ഞങ്ങളുടെ AI അഗ്രോണമിസ്റ്റിൽ നിന്ന് വിശദമായ പ്രവർത്തന പദ്ധതി ലഭിക്കുന്നതിന് നിങ്ങളുടെ വിളയുടെ സാഹചര്യം വിവരിക്കുക.",
        "enter_crop": "1. നിങ്ങളുടെ വിള നൽകുക:",
        "crop_stage": "2. വിളയുടെ ഘട്ടം തിരഞ്ഞെടുക്കുക:",
        "problem_desc": "3. പ്രശ്നം വിവരിക്കുക (ഉദാഹരണത്തിന്, 'താഴത്തെ ഇലകളിൽ മഞ്ഞ പാടുകൾ'):",
        "goal": "4. നിങ്ങളുടെ പ്രാഥമിക ലക്ഷ്യം എന്താണ്?",
        "get_plan_button": "വിദഗ്ദ്ധ പദ്ധതി തയ്യാറാക്കുക",
        "ai_spinner": "🤖 കൃഷിനെറ്റ് AI നിങ്ങളുടെ സാഹചര്യം വിശകലനം ചെയ്യുന്നു...",
        "expert_plan_header": "നിങ്ങളുടെ കസ്റ്റം പ്രവർത്തന പദ്ധതി:",
        "listen_plan": "ഈ പദ്ധതി കേൾക്കുക",
        "audio_spinner": "ഓഡിയോ നിർമ്മിക്കുന്നു...",
        "audio_error": "ക്ഷമിക്കണം, ഓഡിയോ നിർമ്മിക്കാൻ കഴിഞ്ഞില്ല.",
        "chatbot_header": "💬 ദ്രുത ചാറ്റ്",
        "chat_input_placeholder": "ഒരു ദ്രുത ചോദ്യം ചോദിക്കുക...",
        "mandi_header": "ലൈവ് മണ്ഡി വിലകൾ",
        "mandi_desc": "ഏറ്റവും പുതിയ വിലകൾ കാണാൻ നിങ്ങളുടെ സംസ്ഥാനവും ഉൽപ്പന്നവും തിരഞ്ഞെടുക്കുക.",
        "select_state": "സംസ്ഥാനം തിരഞ്ഞെടുക്കുക:",
        "select_commodity": "ഉൽപ്പന്നം തിരഞ്ഞെടുക്കുക:",
        "get_prices_button": "വിലകൾ നേടുക",
        "price_spinner": "ലൈവ് വിലകൾ ലഭ്യമാക്കുന്നു...",
        "disease_header": "🌿 സസ്യരോഗ നിർണയം",
        "disease_desc": "രോഗങ്ങൾ കണ്ടെത്താൻ സസ്യത്തിന്റെ ഇലയുടെ ഒരു ചിത്രം അപ്‌ലോഡ് ചെയ്യുക.",
        "upload_image": "ഒരു ചിത്രം അപ്‌ലോഡ് ചെയ്യുക:",
        "detect_disease_button": "രോഗം കണ്ടെത്തുക",
        "disease_spinner": "ചിത്രം വിശകലനം ചെയ്യുന്നു...",
        "schemes_header": "📜 സർക്കാർ പദ്ധതികൾ കണ്ടെത്തുക",
        "schemes_desc": "നിങ്ങൾക്ക് അനുയോജ്യമായ സർക്കാർ പദ്ധതികൾ കണ്ടെത്താൻ ഞങ്ങളോട് പറയുക.",
        "enter_gender": "നിങ്ങളുടെ ലിംഗഭേദം:",
        "land_holding": "ഭൂമിയുടെ അളവ് (ഏക്കറിൽ):",
        "are_you_loanee": "നിങ്ങൾ മുമ്പ് വായ്പ എടുത്തിട്ടുണ്ടോ?",
        "find_schemes_button": "പദ്ധതികൾ കണ്ടെത്തുക",
        "schemes_spinner": "അനുയോജ്യമായ പദ്ധതികൾ കണ്ടെത്തുന്നു...",
        "recommendations_header": "🌍 വിള ശുപാർശകൾ",
        "recommendations_desc": "നിങ്ങളുടെ പ്രദേശത്തിന് അനുയോജ്യമായ വിള ശുപാർശകൾ ലഭിക്കാൻ നിങ്ങളുടെ സ്ഥലം നൽകുക.",
        "enter_city": "നിങ്ങളുടെ നഗരം നൽകുക:",
        "enter_state": "നിങ്ങളുടെ സംസ്ഥാനം നൽകുക:",
        "get_recommendations_button": "ശുപാർശകൾ നേടുക",
        "recommendations_spinner": "സ്ഥലം വിശകലനം ചെയ്യുന്നു..."
    },

        "tcy": {
        "header": "ಕೃಷಿ ಮಿತ್ರೆ",
        "subheader": "ಭಾರತೊಡು ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ನಿರ್ಧಾರೊಲೆಗ್ ನಿಕ್ಲೆನ AI-ಚಾಲಿತ ಸಹಾಯಕೆ.",
        "bhashabuddy_header": "ಭಾಷಾ ಬಡ್ಡಿ",
        "choose_language": "ಬಾಸೆನ್ ಆಯ್ಕೆ ಮಲ್ಪುಲೆ:",
        "sidebar_info": "ಪೂರ್ತಿ ಭಾಷಾಂತರ ಆಯಿನ ಅನುಭವೊಗು ಬಾಸೆನ್ ಆಯ್ಕೆ ಮಲ್ಪುಲೆ.",
        "tab_expert_diagnosis": "👩‍⚕️ ತಜ್ಞೆರೆನ ರೋಗನಿರ್ಣಯ",
        "tab_mandi": "📈 ಮಂಡಿದ ಬೆಲೆಕುಲು",
        "tab_health": "🌿 ಬುಳೆತ್ತ ಆರೋಗ್ಯ",
        "tab_schemes": "📜 ಸರಕಾರದ ಯೋಜನೆಲು",
        "tab_recommendations": "🌍 ಬುಳೆತ್ತ ಸಲಹೆಲು",
        "expert_header": "🧠 ತಜ್ಞೆರೆನ ರೋಗನಿರ್ಣಯ ಬೊಕ್ಕ ಉತ್ಪಾದಕತೆ ಯೋಜನೆ",
        "expert_desc": "ಎಂಕ್ಲೆನ AI ಕೃಷಿ ವಿಜ್ಞಾನಿಡ್ದ್ ವಿವರವಾಯಿನ ಕ್ರಿಯಾ ಯೋಜನೆನ್ ಪಡೆಯೆರೆ ನಿಕ್ಲೆನ ಬುಳೆತ್ತ ಪರಿಸ್ಥಿತಿನ್ ವಿವರಿಸಾಲೆ.",
        "enter_crop": "1. ನಿಕ್ಲೆನ ಬುಳೆನ್ ಪಾಡ್ಲೆ:",
        "crop_stage": "2. ಬುಳೆತ್ತ ಹಂತೊನು ಆಯ್ಕೆ ಮಲ್ಪುಲೆ:",
        "problem_desc": "3. ಸಮಸ್ಯೆನ್ ವಿವರಿಸಾಲೆ (ಉದಾರ್ಮೆಗ್, 'ತೀರ್ತ್‍ದ ಇರೆಕುಲೆಡ್ ಮಂಜೊಲ್ ಚುಕ್ಕೆಲು'):",
        "goal": "4. ನಿಕ್ಲೆನ ಮುಖ್ಯ ಗುರಿ ದಾನೆ?",
        "get_plan_button": "ತಜ್ಞೆರೆನ ಯೋಜನೆನ್ ರಚಿಸಾಲೆ",
        "ai_spinner": "🤖 ಕೃಷಿನೆಟ್ AI ನಿಕ್ಲೆನ ಪರಿಸ್ಥಿತಿನ್ ವಿಶ್ಲೇಷಣೆ ಮಲ್ತೊಂದುಂಡು...",
        "expert_plan_header": "ನಿಕ್ಲೆನ ಕಸ್ಟಮ್ ಕ್ರಿಯಾ ಯೋಜನೆ:",
        "listen_plan": "ಈ ಯೋಜನೆನ್ ಕೇನುಲೆ",
        "audio_spinner": "ಆಡಿಯೋ ರಚನೆ ಆವೊಂದುಂಡು...",
        "audio_error": "ಕ್ಷಮೆ ოಕೊರು, ಆಡಿಯೋ ರಚನೆ ಮಲ್ಪೆರೆ ಆಯಿಜಿ.",
        "chatbot_header": "💬 വേഗ ചാറ്റ്",
        "chat_input_placeholder": "ಒಂಜಿ വേഗದ ಪ್ರಶ್ನೆ ಕೇನುಲೆ...",
        "mandi_header": "ಲೈವ್ ಮಂಡಿದ ಬೆಲೆಕುಲು",
        "mandi_desc": "ಪೊಸ ಬೆಲೆಕುಲೆನ್ ತೂಯೆರೆ ನಿಕ್ಲೆನ ರಾಜ್ಯ ಬೊಕ್ಕ ವಸ್ತುನು ಆಯ್ಕೆ ಮಲ್ಪುಲೆ.",
        "select_state": "ರಾಜ್ಯೊನು ಆಯ್ಕೆ ಮಲ್ಪುಲೆ:",
        "select_commodity": "ವಸ್ತುನು ಆಯ್ಕೆ ಮಲ್ಪುಲೆ:",
        "get_prices_button": "ಬೆಲೆಕುಲೆನ್ ಪಡೆಯಿರಿ",
        "price_spinner": "ಲೈವ್ ಬೆಲೆಕುಲೆನ್ ಕನವೊಂದುಂಡು...",
        "disease_header": "🌿 ಸಸ್ಯ ರೋಗ ಪತ್ತೆ",
        "disease_desc": "ರೋಗೊಲೆನ್ ಪತ್ತೆ ಮಲ್ಪೆರೆ ಸಸ್ಯದ ಇರೆತ್ತ ಒಂಜಿ ಚಿತ್ರೊನು ಅಪ್‌ಲೋಡ್ ಮಲ್ಪುಲೆ.",
        "upload_image": "ಒಂಜಿ ಚಿತ್ರೊನು ಅಪ್‌ಲೋಡ್ ಮಲ್ಪುಲೆ:",
        "detect_disease_button": "ರೋಗ ಪತ್ತೆ ಮಲ್ಪುಲೆ",
        "disease_spinner": "ಚಿತ್ರೊನು ವಿಶ್ಲೇಷಣೆ ಮಲ್ತೊಂದುಂಡು...",
        "schemes_header": "📜 ಸರಕಾರದ ಯೋಜನೆಲೆನ್ ನಾಡ್ಲೆ",
        "schemes_desc": "ಸಂಬಂಧಪಟ್ಟ ಸರಕಾರದ ಯೋಜನೆಲೆನ್ ನಾಡ್ರೆ ಎಂಕ್ಲೆಗ್ ನಿಕ್ಲೆನ ಬಗ್ಗೆ ಪನ್ಲೆ.",
        "enter_gender": "ನಿಕ್ಲೆನ ಲಿಂಗ:",
        "land_holding": "ಭೂಮಿ (ಎಕರೆಡ್):",
        "are_you_loanee": "ಈ ದುಂಬು ಸಾಲ ದೆತೊಂತೀರಾ?",
        "find_schemes_button": "ಯೋಜನೆಲೆನ್ ನಾಡ್ಲೆ",
        "schemes_spinner": "ಸಂಬಂಧಪಟ್ಟ ಯೋಜನೆಲೆನ್ ನಾಡೊಂದುಂಡು...",
        "recommendations_header": "🌍 ಬುಳೆತ್ತ ಸಲಹೆಲು",
        "recommendations_desc": "ನಿಕ್ಲೆನ ಪ್ರದೇಶೊಗು ಸರಿ ಹೊಂದುನ ಬುಳೆತ್ತ ಸಲಹೆಲೆನ್ ಪಡೆಯೆರೆ ನಿಕ್ಲೆನ ಜಾಗೆನ್ ಪಾಡ್ಲೆ.",
        "enter_city": "ನಿಕ್ಲೆನ ನಗರೊನು ಪಾಡ್ಲೆ:",
        "enter_state": "ನಿಕ್ಲೆನ ರಾಜ್ಯೊನು ಪಾಡ್ಲೆ:",
        "get_recommendations_button": "ಸಲಹೆಲೆನ್ ಪಡೆಯಿರಿ",
        "recommendations_spinner": "ಜಾಗೆನ್ ವಿಶ್ಲೇಷಣೆ ಮಲ್ತೊಂದುಂಡು..."
    },

    "tcy": {
        "header": "ಕೃಷಿಮಿತ್ರ", "subheader": "ಭಾರತೊಡು ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ನಿರ್ಧಾರೊಲೆಗ್ ನಿಕ್ಲೆನ AI-ಚಾಲಿತ ಸಹಾಯಕ.",
        "bhashabuddy_header": "ಭಾಷಾಸಾಥಿ", "choose_language": "ಭಾಷೆನ್ ಆಯ್ಕೆ ಮಲ್ಪುಲೆ:", "sidebar_info": "ಪೂರ್ತಿ ಅನುವಾದ ಆಯಿನ ಅನುಭವೊಗು ಒಂಜಿ ಭಾಷೆನ್ ಆಯ್ಕೆ ಮಲ್ಪುಲೆ.",
        "tab_expert_diagnosis": "👩‍⚕️ ತಜ್ಞೆರೆನ ರೋಗನಿರ್ಣಯ", "tab_mandi": "📈 ಮಂಡಿದ ಬೆಲೆಕುಲು", "tab_health": "🌿 ಬುಳೆತ್ತ ಆರೋಗ್ಯ", "tab_schemes": "📜 ಸರಕಾರಿ ಯೋಜನೆಲು", "tab_recommendations": "🌍 ಬುಳೆತ್ತ ಸಲಹೆಲು",
        "expert_header": "🧠 ತಜ್ಞೆರೆನ ರೋಗನಿರ್ಣಯ ಬೊಕ್ಕ ಉತ್ಪಾದಕತೆ ಯೋಜನೆ", "expert_desc": "ನಮ್ಮ AI ಕೃಷಿ ವಿಜ್ಞಾನಿಡ್ದ್ ವಿವರವಾಯಿನ ಕ್ರಿಯಾ ಯೋಜನೆನ್ ಪಡೆಯೆರೆ ನಿಕ್ಲೆನ ಬುಳೆತ್ತ ಪರಿಸ್ಥಿತಿನ್ ವಿವರಿಸಾಲೆ.",
        "enter_crop": "1. ನಿಕ್ಲೆನ ಬುಳೆನ್ ಪಾಡ್ಲೆ:", "crop_stage": "2. ಬುಳೆತ್ತ ಹಂತೊನು ಆಯ್ಕೆ ಮಲ್ಪುಲೆ:", "problem_desc": "3. ಸಮಸ್ಯೆನ್ ವಿವರಿಸಾಲೆ (ಉದಾಹರಣೆಗೆ, 'ತಿರ್ತ್‌ದ ಇರೆಕುಲೆಡ್ ಮಂಜೊಲ್ ಚುಕ್ಕೆಲು'):",
        "goal": "4. ನಿಕ್ಲೆನ ಮುಖ್ಯ ಗುರಿ ದಾದಾ?", "get_plan_button": "ತಜ್ಞೆರೆನ ಯೋಜನೆನ್ ರಚನೆ ಮಲ್ಪುಲೆ", "ai_spinner": "🤖 ಕೃಷಿನೆಟ್ AI ನಿಕ್ಲೆನ ಪರಿಸ್ಥಿತಿನ್ ವಿಶ್ಲೇಷಣೆ ಮಲ್ತೊಂದುಂಡು...",
        "expert_plan_header": "ನಿಕ್ಲೆನ ಕಸ್ಟಮ್ ಕ್ರಿಯಾ ಯೋಜನೆ:", "listen_plan": "ಈ ಯೋಜನೆನ್ ಕೇನುಲೆ", "audio_spinner": "ಆಡಿಯೋ ರಚನೆ ಆವೊಂದುಂಡು...", "audio_error": "ಕ್ಷಮೆ ಮಲ್ಪುಲೆ, ಆಡಿಯೋ ರಚನೆ ಮಲ್ಪರೆ ಆಯಿಜಿ.",
        "chatbot_header": "💬 ಬೇಗೊದ ಚಾಟ್", "chat_input_placeholder": "ಒಂಜಿ ಬೇಗೊದ ಪ್ರಶ್ನೆ ಕೇನುಲೆ...",
        "mandi_header": "లైవ్ ಮಂಡಿದ ಬೆಲೆಕುಲು", "mandi_desc": "ಪೊಸ ಬೆಲೆಕುಲೆನ್ ತೂವರೆ ನಿಕ್ಲೆನ ರಾಜ್ಯ ಬೊಕ್ಕ ವಸ್ತುನು ಆಯ್ಕೆ ಮಲ್ಪುಲೆ.", "select_state": "ರಾಜ್ಯ ಆಯ್ಕೆ ಮಲ್ಪುಲೆ:", "select_commodity": "ವಸ್ತು ಆಯ್ಕೆ ಮಲ್ಪುಲೆ:", "get_prices_button": "ಬೆಲೆಕುಲೆನ್ ಪಡೆಯಿರಿ",
        "price_spinner": "ಲೈವ್ ಬೆಲೆಕುಲೆನ್ ಕನವೊಂದುಂಡು...", "disease_header": "🌿 ಸಸ್ಯ ರೋಗ ಪತ್ತೆ", "disease_desc": "ರೋಗೊಲೆನ್ ಪತ್ತೆ ಮಲ್ಪರೆ ಸಸ್ಯದ ಇರೆತ್ತ ಒಂಜಿ ಫೋಟೋನು ಅಪ್ಲೋಡ್ ಮಲ್ಪುಲೆ.", "upload_image": "ಒಂಜಿ ಫೋಟೋನು ಅಪ್ಲೋಡ್ ಮಲ್ಪುಲೆ:",
        "detect_disease_button": "ರೋಗ ಪತ್ತೆ ಮಲ್ಪುಲೆ", "disease_spinner": "ಫೋಟೋನು ವಿಶ್ಲೇಷಣೆ ಮಲ್ತೊಂದುಂಡು...",
        "schemes_header": "📜 ಸರಕಾರಿ ಯೋಜನೆಲೆನ್ ನಾಡ್ಲೆ", "schemes_desc": "ಸಂಬಂಧಪಟ್ಟ ಸರಕಾರಿ ಯೋಜನೆಲೆನ್ ನಾಡರೆ ನಮ್ಮೊಟ್ಟು ನಿಕ್ಲೆನ ಬಗ್ಗೆ ಪನ್ಲೆ.", "enter_gender": "ನಿಕ್ಲೆನ ಲಿಂಗ:", "land_holding": "ಭೂಮಿದ পরিমাণ (ಎಕರೆಡ್):",
        "are_you_loanee": "ಈಕ್ ದುಂಬು ಸಾಲ ದೆತೊಂತೀರಾ?", "find_schemes_button": "ಯೋಜನೆಲೆನ್ ನಾಡ್ಲೆ", "schemes_spinner": "ಸಂಬಂಧಪಟ್ಟ ಯೋಜನೆಲೆನ್ ನಾಡೊಂದುಂಡು...",
        "recommendations_header": "🌍 ಬುಳೆತ್ತ ಸಲಹೆಲು", "recommendations_desc": "ನಿಕ್ಲೆನ ಪ್ರದೇಶೊಗು ಸರಿ ಹೊಂದುನ ಬುಳೆತ್ತ ಸಲಹೆಲೆನ್ ಪಡೆಯೆರೆ ನಿಕ್ಲೆನ ಜಾಗೆನ್ ಪಾಡ್ಲೆ.", "enter_city": "ನಿಕ್ಲೆನ ನಗರೊನು ಪಾಡ್ಲೆ:",
        "enter_state": "ನಿಕ್ಲೆನ ರಾಜ್ಯೊನು ಪಾಡ್ಲೆ:", "get_recommendations_button": "ಸಲಹೆಲೆನ್ ಪಡೆಯಿರಿ", "recommendations_spinner": "ಜಾಗೆನ್ ವಿಶ್ಲೇಷಣೆ ಮಲ್ತೊಂದುಂಡು..."
    },
    
    "mni": {
        "header": "কৃষি মিত্র",
        "subheader": "ভারততা স্মার্ট লৌউ-শিংউগী ৱারেপ লৌবদা মতেং পাংনবা নহাক্কী AI-চಾಲিত মতেং পাংবীবনি।",
        "bhashabuddy_header": "ভাষা বডি",
        "choose_language": "লোন খল্লু:",
        "sidebar_info": "মপুং ফাবা ওন্থোকপীবা অৱাবা অমগীদমক লোন খল্লু।",
        "tab_expert_diagnosis": "👩‍⚕️ মশক খঙবা মীহুৎকী নিদান",
        "tab_mandi": "📈 মন্দিগী মমল",
        "tab_health": "🌿 মহৈ-মরোংগী হকশেল",
        "tab_schemes": "📜 সরকারী স্কিমশিং",
        "tab_recommendations": "🌍 মহৈ-মরোংগী রিকমেন্ডেশনশিং",
        "expert_header": "🧠 মশক খঙবা মীহুৎকী নিদান অমসুং পোত্থোক পুথোকপগী প্লান",
        "expert_desc": "ঐখোয়গী AI এগ্রোনোমিষ্টতগী মথং-মথং চৎকদবা থবক্কী প্লান ফংনবা নহাক্কী মহৈ-মরোংগী ফিভম পল্লি।",
        "enter_crop": "১. নহাক্কী মহৈ-মরোং ইন্টর তৌ:",
        "crop_stage": "২. মহৈ-মরোংগী থাক খল্লু:",
        "problem_desc": "৩. খুদোংচাবা পল্লি (খুদম ওইনা, 'মখাগী মনাশিংদা অঙৌবা মচু খরা লৈ'):",
        "goal": "৪. নহাক্কী মরুওইবা পান্দম করিনো?",
        "get_plan_button": "মশক খঙবা মীহুৎকী প্লান শেমগৎলু",
        "ai_spinner": "🤖 কৃষিনেট AIনা নহাক্কী ফিভম চাংয়েংলি...",
        "expert_plan_header": "নহাক্কী কাস্টম থবক্কী প্লান:",
        "listen_plan": "প্লান অসি তাউ",
        "audio_spinner": "অডিও শেমগৎলি...",
        "audio_error": "ঙাকপীয়ু, অডিও শেমগৎপা ঙমদ্রে।",
        "chatbot_header": "💬 অথুবা ৱারী শান্নবা",
        "chat_input_placeholder": "অথুবা ৱাহং অমা হংঙু...",
        "mandi_header": "লাইভ মন্দিগী মমলশিং",
        "mandi_desc": "অনৌবা মমলশিং উবা ফংনবা নহাক্কী রাজ্য অমসুং পোত্থোক খল্লু।",
        "select_state": "রাজ্য খল্লু:",
        "select_commodity": "পোত্থোক খল্লু:",
        "get_prices_button": "মমল ফংঙু",
        "price_spinner": "লাইভ মমলশিং পুরক্লি...",
        "disease_header": "🌿 পাম্বীগী লাইনা খঙদোকপা",
        "disease_desc": "লাইনা খঙদোকনবা পাম্বীগী মনাগী ফটো অমা আপলোড তৌ।",
        "upload_image": "ফটো অমা আপলোড তৌ:",
        "detect_disease_button": "লাইনা খঙদোকউ",
        "disease_spinner": "ফটো চাংয়েংলি...",
        "schemes_header": "📜 সরকারী স্কিমশিং থিবীব",
        "schemes_desc": "মরিলৈনবা সরকারী স্কিমশিং ফংনবা ঐখোয়দা নহাক্কী মরমদা খরা হায়বীয়ু।",
        "enter_gender": "নহাক্কী লিঙ্গ:",
        "land_holding": "লম পায়বা (একরদা):",
        "are_you_loanee": "নহাক্না মমাংদা লোন লৌখ্রবরা?",
        "find_schemes_button": "স্কিমশিং থিউ",
        "schemes_spinner": "মরিলৈনবা স্কিমশিং থিবা চত্থরি...",
        "recommendations_header": "🌍 মহৈ-মরোংগী রিকমেন্ডেশনশিং",
        "recommendations_desc": "নহাক্কী লমদমগীদমক চুনবা মহৈ-মরোংগী রিকমেন্ডেশন ফংনবা নহাক্কী মফম ইন্টর তৌ।",
        "enter_city": "নহাক্কী শহর ইন্টর তৌ:",
        "enter_state": "নহাক্কী রাজ্য ইন্টর তৌ:",
        "get_recommendations_button": "রিকমেন্ডেশন ফংঙু",
        "recommendations_spinner": "মফম চাংয়েংলি..."
    },
        
}



# --- 4. UI RENDER: SIDEBAR ---
with st.sidebar:
    st.header(translations["en"]["bhashabuddy_header"] + " (" + translations["hi"]["bhashabuddy_header"] + ")")
    language_options = {
        "English": "en", "हिन्दी (Hindi)": "hi", "বাংলা (Bengali)": "bn", "অসমীয়া (Assamese)": "as", "ଓଡ଼ିଆ (Odia)": "or" , "తెలుగు (Telugu)": "te",
        "मराठी (Marathi)": "mr", "தமிழ் (Tamil)": "ta", "ગુજરાતી (Gujarati)": "gu", "ಕನ್ನಡ (Kannada)": "kn",
        "ਪੰਜਾਬੀ (Punjabi)": "pa"
    }
    selected_language_name = st.selectbox("Choose Language:", list(language_options.keys()))
    selected_language_code = language_options.get(selected_language_name, "en")
    t = translations.get(selected_language_code, translations["en"])
    st.markdown("---")
    st.info(t["sidebar_info"])

# --- 5. UI RENDER: MAIN PAGE HEADER ---
st.title(f"🌾 {t['header']}")
st.markdown(f"#### {t['subheader']}")

# --- 6. UI RENDER: TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    t["tab_expert_diagnosis"], t["tab_mandi"], t["tab_health"], t["tab_schemes"], t["tab_recommendations"]
])

# --- TAB 1: EXPERT DIAGNOSIS ---
with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        with st.container(border=True):
            st.header(t["expert_header"])
            st.markdown(t["expert_desc"])

            expert_crop = st.text_input(t["enter_crop"], "Tomato")
            expert_stage = st.selectbox(t["crop_stage"], ["Sowing", "Vegetative Growth", "Flowering", "Harvesting"])
            expert_problem = st.text_area(t["problem_desc"], "Yellow spots with brown edges on lower leaves.")
            expert_goal = st.selectbox(t["goal"], ["Increase Yield", "Improve Quality", "Reduce Costs", "Control Pests"])

            if st.button(t["get_plan_button"], use_container_width=True, type="primary"):
                api_endpoint = f"{BACKEND_URL}/api/v1/expert_advice"
                payload = { "crop": expert_crop, "crop_stage": expert_stage, "problem_description": expert_problem, "goal": expert_goal, "lang": selected_language_code }
                try:
                    with st.spinner(t["ai_spinner"]):
                        response = requests.post(api_endpoint, json=payload, timeout=90)
                        response.raise_for_status()
                        st.session_state.expert_plan = response.json()
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection Error: {e}")

        if 'expert_plan' in st.session_state:
            st.markdown("---")
            st.subheader(t["expert_plan_header"])
            plan_data = st.session_state.expert_plan.get("plan", {})
            
            if isinstance(plan_data, dict):
                st.info(f"**Diagnosis:** {plan_data.get('diagnosis', 'N/A')}")
                st.success("**Action Plan:**")
                for step in plan_data.get('action_plan', []): st.markdown(f"- {step}")
                st.warning("**Preventative Measures:**")
                st.markdown(f"- {plan_data.get('preventative_measures', 'N/A')}")

                full_plan_text = f"Diagnosis: {plan_data.get('diagnosis', '')}. Action Plan: {'. '.join(plan_data.get('action_plan', []))}. Preventative Measures: {plan_data.get('preventative_measures', '')}"
                if st.button(t["listen_plan"]):
                    with st.spinner(t["audio_spinner"]):
                        audio_response = requests.get(f"{BACKEND_URL}/api/v1/generate_audio", params={"text": full_plan_text, "lang": selected_language_code})
                        if audio_response.status_code == 200: st.audio(BytesIO(audio_response.content), format='audio/mpeg')
                        else: st.error(t["audio_error"])
            else:
                st.markdown(st.session_state.expert_plan.get("advice", "Could not parse the plan."))

    with col2:
        with st.container(border=True):
            st.header(t["chatbot_header"])
            if "messages" not in st.session_state: st.session_state.messages = []
            for message in st.session_state.messages:
                with st.chat_message(message["role"]): st.markdown(message["content"])

            if prompt := st.chat_input(t["chat_input_placeholder"]):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"): st.markdown(prompt)
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = requests.post(
                            f"{BACKEND_URL}/api/v1/chatbot", 
                            json={"user_message": prompt, "history": st.session_state.messages, "language": selected_language_code}
                        )
                        full_response = response.json().get("response", "Sorry, I had trouble processing that.")
                        st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- TAB 2: MANDI PRICES ---
# --- TAB 2: MANDI PRICES ---
with tab2:
    st.header(t["mandi_header"])
    st.markdown(t["mandi_desc"])

    # Define the inputs
    states = ["Rajasthan", "Punjab", "Uttar Pradesh", "Madhya Pradesh", "Maharashtra"]
    commodities = ["Wheat", "Mustard", "Rice", "Maize", "Cotton", "Soybean"]
    
    col1, col2 = st.columns(2)
    with col1:
        selected_state = st.selectbox(t["select_state"], states, key="mandi_state")
    with col2:
        selected_commodity = st.selectbox(t["select_commodity"], commodities, key="mandi_commodity")
    
    # The button to trigger the API call
    if st.button(t["get_prices_button"], use_container_width=True):
        with st.spinner(t["price_spinner"]):
            try:
                # Make the API call to the backend
                response = requests.get(
                    f"{BACKEND_URL}/api/v1/mandi_prices", 
                    params={"state": selected_state, "commodity": selected_commodity}
                )
                response.raise_for_status() # Raise an error for bad responses (4xx or 5xx)
                
                # Store the result in session state
                st.session_state.mandi_data = response.json()

            except requests.exceptions.RequestException as e:
                st.error(f"Could not fetch prices. Error: {e}")
                st.session_state.mandi_data = None

    # --- Display Area for the results ---
    # This part of the code runs every time, but only shows data if it exists.
    if 'mandi_data' in st.session_state and st.session_state.mandi_data:
        st.markdown("---")
        st.subheader(f"Showing Prices for {selected_commodity} in {selected_state}")
        
        price_list = st.session_state.mandi_data.get("prices", [])
        
        if price_list:
            # Use pandas DataFrame for a beautiful, sortable table
            df = pd.DataFrame(price_list)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No price data is available for this commodity in the selected state.")

# --- TAB 3: CROP HEALTH (DISEASE DETECTION) ---
with tab3:
    st.header(t["disease_header"])
    st.markdown(t["disease_desc"])
    uploaded_file = st.file_uploader(t["upload_image"], type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Leaf Image.", use_column_width=True)
        if st.button(t["detect_disease_button"], use_container_width=True):
            with st.spinner(t["disease_spinner"]):
                try:
                    files = {'image': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(f"{BACKEND_URL}/api/v1/detect_disease", files=files)
                    response.raise_for_status()
                    data = response.json()
                    st.success(f"**Detected Disease:** {data.get('disease', 'Unknown')} (Confidence: {data.get('confidence', 'N/A')}%)")
                except requests.exceptions.RequestException as e: st.error(f"Could not analyze image: {e}")

# --- TAB 4: GOVT. SCHEMES ---
with tab4:
    st.header(t["schemes_header"])
    st.markdown(t["schemes_desc"])
    with st.container(border=True):
        gender = st.selectbox(t["enter_gender"], ["Male", "Female", "Other"])
        land_holding = st.number_input(t["land_holding"], min_value=0.0, step=0.5, value=2.5)
        is_loanee = st.checkbox(t["are_you_loanee"])
        if st.button(t["find_schemes_button"], use_container_width=True):
            with st.spinner(t["schemes_spinner"]):
                try:
                    payload = {"gender": gender, "land_holding_acres": land_holding, "is_loanee": is_loanee}
                    response = requests.post(f"{BACKEND_URL}/api/v1/govt_schemes", json=payload, params={"lang": selected_language_code})
                    response.raise_for_status()
                    data = response.json()
                    st.subheader("Recommended Schemes for You:")
                    if data.get("schemes"):
                        for scheme in data.get("schemes", []): st.success(scheme)
                    else:
                        st.warning("No specific schemes found based on your profile.")
                except requests.exceptions.RequestException as e: st.error(f"Could not find schemes: {e}")

# --- TAB 5: CROP RECOMMENDATIONS ---
with tab5:
    st.header(t["recommendations_header"])
    st.markdown(t["recommendations_desc"])
    with st.container(border=True):
        city = st.text_input(t["enter_city"], "Udaipur")
        state = st.text_input(t["enter_state"], "Rajasthan")
        if st.button(t["get_recommendations_button"], use_container_width=True):
            with st.spinner(t["recommendations_spinner"]):
                try:
                    response = requests.get(f"{BACKEND_URL}/api/v1/crop_recommendation", params={"city": city, "state": state})
                    response.raise_for_status()
                    data = response.json()
                    st.success(f"**Agro-Climatic Zone:** {data.get('location', {}).get('agro_climatic_zone', 'N/A')}")
                    st.subheader("Recommended Crops for Your Region:")
                    if data.get("recommended_crops"):
                        for crop in data.get("recommended_crops", []): st.markdown(f"- {crop}")
                    else:
                        st.warning("Could not determine recommendations for this location.")
                except requests.exceptions.RequestException as e: st.error(f"Could not get recommendations: {e}")