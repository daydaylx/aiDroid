import requests
import json
from kivy.logger import Logger

def fetch_models(api_key):
    """Verfügbare Modelle von OpenRouter holen"""
    url = "https://openrouter.ai/api/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "OpenRouter CodeGen"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        models = data.get("data", [])
        
        # Nur Code-taugliche Modelle filtern
        code_models = []
        for model in models:
            model_id = model.get("id", "")
            if any(x in model_id.lower() for x in [
                "gpt", "claude", "deepseek", "codellama", 
                "qwen", "llama", "mistral", "gemini"
            ]):
                code_models.append(model_id)
        
        return sorted(code_models)
        
    except requests.RequestException as e:
        Logger.error(f"Fehler beim Laden der Modelle: {e}")
        raise Exception(f"Netzwerkfehler: {e}")
    except Exception as e:
        Logger.error(f"Allgemeiner Fehler: {e}")
        raise Exception(f"Fehler beim Verarbeiten der Modelle: {e}")

def generate_code(api_key, model, system_prompt, user_prompt):
    """Code über OpenRouter generieren"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "OpenRouter CodeGen"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 2048
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        return content
        
    except requests.RequestException as e:
        Logger.error(f"API Request Fehler: {e}")
        raise Exception(f"OpenRouter API Fehler: {e}")
    except KeyError as e:
        Logger.error(f"Response Format Fehler: {e}")
        raise Exception("Unerwartete API Antwort")
    except Exception as e:
        Logger.error(f"Allgemeiner Fehler: {e}")
        raise Exception(f"Fehler bei Code-Generierung: {e}")
