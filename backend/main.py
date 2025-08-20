# backend/main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List

# Import all feature modules
from .features import (
    weather, agri_advisor, location_info, mandi_prices, 
    disease_detection, govt_schemes, tts, chatbot, productivity_booster # <-- NEW IMPORT
)

app = FastAPI()

# --- Pydantic Models for API Request Bodies ---
class ChatMessage(BaseModel):
    user: str
    assistant: str

class ChatRequest(BaseModel):
    user_message: str
    history: List[ChatMessage] = []
    language: str = 'en'

class FarmerProfile(BaseModel):
    gender: str | None = None
    land_holding_acres: float | None = None
    is_loanee: bool | None = None

class ExpertAdviceRequest(BaseModel): # <-- NEW MODEL
    crop: str
    crop_stage: str
    problem_description: str
    goal: str
    lang: str = 'en'

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"Project": "KrishiMitra 2.0+ Backend"}

@app.get("/api/v1/weather")
def get_weather(city: str = "Udaipur", state: str = "Rajasthan"):
    return weather.get_weather_data(city, state)

@app.get("/api/v1/agri_advice")
async def get_agri_advice(city: str = "Udaipur", state: str = "Rajasthan", crop: str = "wheat", crop_stage: str = "Sowing", lang: str = "en"):
    return await agri_advisor.generate_agri_advice(city, state, crop, crop_stage, lang)

# --- NEW: Expert Diagnosis & Productivity Endpoint ---
@app.post("/api/v1/expert_advice")
async def get_expert_advice(request: ExpertAdviceRequest):
    """
    Provides a detailed, multi-part plan based on specific farmer inputs.
    """
    return await productivity_booster.generate_expert_advice(
        crop=request.crop,
        crop_stage=request.crop_stage,
        problem_description=request.problem_description,
        goal=request.goal,
        lang=request.lang
    )

# ... (all other endpoints remain the same) ...

@app.get("/api/v1/crop_recommendation")
def get_crop_recommendation(city: str = "Udaipur", state: str = "Rajasthan"):
    zone_name = location_info.get_agro_climatic_zone_name(city, state)
    recommended_crops = location_info.get_recommended_crops(city, state)
    return {
        "location": {"city": city, "state": state, "agro_climatic_zone": zone_name},
        "recommended_crops": recommended_crops
    }

@app.get("/api/v1/mandi_prices")
def get_mandi_prices(state: str = "Rajasthan", commodity: str = "Wheat"):
    return mandi_prices.get_live_prices_for_commodity(state, commodity)

@app.post("/api/v1/detect_disease")
async def detect_disease(image: UploadFile = File(...)):
    return disease_detection.simulate_disease_detection(image)

@app.post("/api/v1/govt_schemes")
def get_govt_schemes(profile: FarmerProfile, state: str = "Rajasthan", lang: str = "en"):
    farmer_profile_dict = profile.dict(exclude_none=True)
    return govt_schemes.get_schemes_for_farmer(state, farmer_profile_dict, lang)

@app.get("/api/v1/generate_audio")
def generate_audio(text: str = "Welcome to KrishiMitra", lang: str = "en"):
    audio_stream = tts.generate_audio_from_text(text, lang)
    if audio_stream:
        return StreamingResponse(audio_stream, media_type="audio/mpeg")
    return {"error": "Could not generate audio."}

@app.post("/api/v1/chatbot")
async def handle_chat(chat_request: ChatRequest):
    history_dicts = [item.dict() for item in chat_request.history]
    return await chatbot.generate_chatbot_response(
        user_message=chat_request.user_message,
        history=history_dicts,
        language=chat_request.language
    )
