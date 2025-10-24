# helper/gemini_helper.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env
load_dotenv()

# Configure Gemini API key once
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Helper for email body
def generate_email_with_gemini(prompt: str) -> str:
    # Updated to use current stable model
    model = genai.GenerativeModel(model_name="gemini-2.5-flash") 
    try:
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)
    except Exception as e:
        return f"[Gemini API Error]: {e}"

# Helper for AI-generated image descriptions
def generate_image_description_with_gemini(topic, context, goal) -> str:
    prompt = (
        f"Given the following email topic: '{topic}'.\n"
        f"Context: '{context}'.\n"
        f"Goal: '{goal}'.\n"
        "Suggest a concise, vivid, photorealistic image description to visually represent this email, ready for image-generation AI. "
        "Do NOT use placeholder text. Write as a full descriptive sentence."
    )
    try:
        # Updated to use current stable model
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text.replace('\n', ' ').strip()
    except Exception as e:
        return "Business meeting, handshake, office."
