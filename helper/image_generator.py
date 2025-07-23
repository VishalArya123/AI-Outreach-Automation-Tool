import os
import requests
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")

def generate_image(prompt: str, output_file="generated_image.png") -> str:
    url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    try:
        response = requests.post(url, headers=headers, json={"inputs": prompt})
        if response.status_code != 200:
            raise Exception(response.json())
        with open(output_file, "wb") as f:
            f.write(response.content)
        return output_file
    except Exception as e:
        print(f"[Image Generation Error]: {e}")
        return None
