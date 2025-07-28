import time
from google.api_core.exceptions import ResourceExhausted

MODEL_PRIORITY = [
    "models/gemini-2.5-flash",
    "models/gemini-2.5-flash-preview-05-20",
    "models/gemini-2.5-flash-lite",
    "models/gemini-2.5-flash-lite-preview-06-17",
    "models/gemini-1.5-flash-002",
    "models/gemini-1.5-flash",
    "models/gemini-1.5-flash-latest",
    "models/gemini-1.5-flash-8b-latest",
    "models/gemini-1.5-flash-8b-001",
    "models/gemini-1.5-flash-8b",
    "models/gemini-2.0-flash",
    "models/gemini-2.0-flash-001",
    "models/gemini-2.0-flash-lite",
    "models/gemini-2.0-flash-lite-001",
    "models/gemini-2.0-flash-lite-preview-02-05",
    "models/gemini-2.0-flash-lite-preview",
    "models/gemini-2.5-pro",                       
    "models/gemini-2.5-pro-preview-06-05",
    "models/gemini-2.5-pro-preview-05-06",
    "models/gemini-2.5-pro-preview-03-25",
    "models/gemini-2.0-pro-exp",
    "models/gemini-1.5-pro-002",
    "models/gemini-1.5-pro",
    "models/gemini-1.5-pro-latest",
    "models/gemini-2.0-pro-exp-02-05",
    "models/gemini-2.0-flash-exp",
    "models/gemini-2.0-flash-thinking-exp-01-21",
    "models/gemini-2.0-flash-thinking-exp",
    "models/gemini-2.0-flash-thinking-exp-1219",
]

def safe_generate_content(client, prompt, model_list=MODEL_PRIORITY, **kwargs):
    for model_name in model_list:
        try:
            print(f"Trying with model: {model_name}")
            model = client.GenerativeModel(model_name)
            response = model.generate_content(prompt, **kwargs)
            return response.text
        except ResourceExhausted as e:
            print(f"Quota limit reached on {model_name}, trying next model...")
            time.sleep(1)  
        except Exception as e:
            print(f"Error on {model_name}: {type(e).__name__} - {e}")

    return "Semua model saat ini melebihi kuota atau error. Coba lagi nanti."