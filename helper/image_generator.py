import os
import requests
from dotenv import load_dotenv
import random

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")

# Fallback images array
FALLBACK_IMAGES = [
    {
        "url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3",
        "description": "A person working on a laptop in a modern office, ideal for drafting professional emails."
    },
    {
        "url": "https://images.unsplash.com/photo-1460925895917-afdab8276846",
        "description": "A desk with a laptop and coffee, symbolizing a workspace for writing follow-up emails."
    },
    {
        "url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
        "description": "A professional office setup, evoking the context of sending reminder emails."
    },
    {
        "url": "https://images.unsplash.com/photo-1516321497487-9b3b92b3b3b3",
        "description": "A team collaborating in a meeting, reflecting professional introductions."
    },
    {
        "url": "https://images.unsplash.com/photo-1505238680359-1e77e6c0f7e9",
        "description": "A person checking their phone, suggesting email communication on the go."
    },
    {
        "url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40",
        "description": "A clean workspace with a computer, perfect for composing introduction emails."
    },
    {
        "url": "https://images.unsplash.com/photo-1517245386807-9b3b3b3b3b3e",
        "description": "Hands typing on a keyboard, representing the act of drafting emails."
    },
    {
        "url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c",
        "description": "A group working together, symbolizing teamwork and follow-up discussions."
    },
    {
        "url": "https://images.unsplash.com/photo-1516321318423-24b3b92b3b3e",
        "description": "A coffee shop workspace with a laptop, evoking remote email communication."
    },
    {
        "url": "https://images.unsplash.com/photo-1517048676732-d65bc937f952",
        "description": "People shaking hands, representing professional introductions and networking."
    }
]

# def generate_image(prompt: str, output_file="generated_image.png") -> tuple:
#     """
#     Generate an image using Hugging Face's new Inference Providers API.
#     Updated to use the new router.huggingface.co endpoint.
#     """
#     # NEW ENDPOINT - Updated from api-inference.huggingface.co to router.huggingface.co
#     url = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev"
#     headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
#     try:
#         response = requests.post(url, headers=headers, json={"inputs": prompt})
        
#         if response.status_code != 200:
#             error = response.json()
#             if 'error' in error and 'exceeded your monthly included credits' in error['error']:
#                 # Shuffle fallback images to try randomly
#                 shuffled_images = FALLBACK_IMAGES.copy()
#                 random.shuffle(shuffled_images)
#                 for fallback_image in shuffled_images:
#                     try:
#                         print(f"[Image Generation Error]: {error}. Attempting to download fallback image: {fallback_image['description']}")
#                         # Download the fallback image
#                         fallback_response = requests.get(fallback_image['url'], timeout=10)
#                         if fallback_response.status_code == 200:
#                             with open(output_file, "wb") as f:
#                                 f.write(fallback_response.content)
#                             return output_file, fallback_image['description']
#                         else:
#                             print(f"[Image Generation Error]: Failed to download fallback image from {fallback_image['url']} with status code {fallback_response.status_code}")
#                     except Exception as download_error:
#                         print(f"[Image Generation Error]: Failed to download fallback image from {fallback_image['url']}: {download_error}")
#                         continue
#                 raise Exception("All fallback image downloads failed.")
#             raise Exception(error)
        
#         with open(output_file, "wb") as f:
#             f.write(response.content)
#         return output_file, None
        
#     except Exception as e:
#         print(f"[Image Generation Error]: {e}")
#         return None, None


# ALTERNATIVE METHOD: Using the new InferenceClient (Recommended for production)
# Uncomment the code below to use this method instead

# """
from huggingface_hub import InferenceClient

def generate_image(prompt: str, output_file="generated_image.png") -> tuple:
    '''
    Generate an image using Hugging Face's InferenceClient.
    This is the recommended method for the new Inference Providers API.
    '''
    try:
        client = InferenceClient(
            api_key=HF_TOKEN,
            provider="hf-inference"  # Explicitly use hf-inference provider
        )
        
        # Generate image using text_to_image method
        image = client.text_to_image(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-dev"
        )
        
        # Save the PIL Image object to file
        image.save(output_file)
        return output_file, None
        
    except Exception as e:
        error_msg = str(e)
        if 'exceeded your monthly included credits' in error_msg or 'quota' in error_msg.lower():
            # Shuffle fallback images to try randomly
            shuffled_images = FALLBACK_IMAGES.copy()
            random.shuffle(shuffled_images)
            for fallback_image in shuffled_images:
                try:
                    print(f"[Image Generation Error]: {error_msg}. Attempting to download fallback image: {fallback_image['description']}")
                    fallback_response = requests.get(fallback_image['url'], timeout=10)
                    if fallback_response.status_code == 200:
                        with open(output_file, "wb") as f:
                            f.write(fallback_response.content)
                        return output_file, fallback_image['description']
                    else:
                        print(f"[Image Generation Error]: Failed to download fallback image from {fallback_image['url']} with status code {fallback_response.status_code}")
                except Exception as download_error:
                    print(f"[Image Generation Error]: Failed to download fallback image from {fallback_image['url']}: {download_error}")
                    continue
            
        print(f"[Image Generation Error]: {e}")
        return None, None
# """
