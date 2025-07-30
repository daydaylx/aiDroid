import json
import logging
import os
import time
import requests
from pathlib import Path
from typing import List, Callable, Optional
import threading
from memory import memory

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('OpenRouter.log'), logging.StreamHandler()]
)
logger = logging.getLogger("openrouter")

CACHE_DIR = Path.home() / ".cache" / "openrouter"
MODELS_CACHE = CACHE_DIR / "models.json"
CACHE_TTL = 24 * 3600
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def _is_cache_valid() -> bool:
    return MODELS_CACHE.exists() and (time.time() - MODELS_CACHE.stat().st_mtime < CACHE_TTL)

def fetch_models(api_key: str) -> List[str]:
    if not api_key or not api_key.strip():
        raise ValueError("API Key fehlt")
    if _is_cache_valid():
        try:
            logger.info("Lade Modelle aus Cache")
            with open(MODELS_CACHE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Cache-Fehler, lade von API: {e}")
    logger.info("Lade Modelle von OpenRouter API")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        r = requests.get("https://openrouter.ai/api/v1/models", headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        good_models = []
        all_models = []
        for model in data.get("data", []):
            model_id = model["id"]
            all_models.append(model_id)
            if any(x in model_id.lower() for x in ["claude", "gpt-4", "deepseek-coder", "qwen", "llama-3"]):
                good_models.append(model_id)
        models = good_models[:10] + [m for m in all_models[:30] if m not in good_models]
        with open(MODELS_CACHE, 'w', encoding='utf-8') as f:
            json.dump(models, f, indent=2)
        logger.info(f"Gefunden: {len(models)} Modelle")
        return models
    except Exception as e:
        raise Exception("Fehler beim Laden der Modelle: " + str(e))

def generate_code_stream_with_memory(
    api_key: str, model: str, system_prompt: str, user_prompt: str,
    callback: Callable[[str], None], stop_event: Optional[threading.Event] = None,
    use_context: bool = True, project_context: str = "", save_to_memory: bool = True,
) -> str:
    if not all([api_key, model, user_prompt]):
        raise ValueError("API Key, Modell und Prompt sind erforderlich")
    enhanced_system_prompt = system_prompt
    if use_context:
        context = memory.get_conversation_context(last_n=3)
        if context:
            enhanced_system_prompt += f"\n\n{context}"
        if project_context:
            proj_ctx = memory.get_project_context(project_context)
            if proj_ctx:
                enhanced_system_prompt += f"\n\nPROJEKT-KONTEXT: {json.dumps(proj_ctx, indent=2)}"
        similar = memory.find_similar_conversations(user_prompt, limit=2)
        if similar:
            enhanced_system_prompt += "\n\nÄHNLICHE FRÜHERE LÖSUNGEN:\n"
            for i, conv in enumerate(similar, 1):
                enhanced_system_prompt += f"{i}. {conv['user_prompt'][:100]}... -> {conv['generated_code'][:200]}...\n"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": enhanced_system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 4000,
        "temperature": 0.7,
        "top_p": 0.9,
        "stream": True
    }
    full_response = ""
    try:
        logger.info(f"Starte Streaming-Generation mit Memory-Kontext")
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload, headers=headers, timeout=60, stream=True
        )
        r.raise_for_status()
        for line in r.iter_lines():
            if stop_event and stop_event.is_set():
                logger.info("Stream-Generation gestoppt")
                break
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data_str = line[6:]
                    if data_str.strip() == '[DONE]':
                        break
                    try:
                        data = json.loads(data_str)
                        if 'choices' in data and data['choices']:
                            delta = data['choices'][0].get('delta', {})
                            if 'content' in delta:
                                chunk = delta['content']
                                full_response += chunk
                                callback(chunk)
                    except json.JSONDecodeError:
                        continue
        if save_to_memory and full_response:
            memory.add_conversation(
                user_prompt=user_prompt,
                generated_code=full_response,
                system_prompt=system_prompt,
                model_used=model,
                project_context=project_context,
                tags=["streaming", "code-generation"]
            )
        logger.info("Streaming-Generation mit Memory erfolgreich abgeschlossen")
        return full_response
    except Exception as e:
        logger.error(f"Streaming-Generation mit Memory fehlgeschlagen: {e}")
        raise

def generate_code(api_key: str, model: str, system_prompt: str, user_prompt: str) -> str:
    enhanced_system_prompt = system_prompt
    context = memory.get_conversation_context(last_n=3)
    if context:
        enhanced_system_prompt += f"\n\n{context}"
    if not all([api_key, model, user_prompt]):
        raise ValueError("API Key, Modell und Prompt sind erforderlich")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": enhanced_system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 4000,
        "temperature": 0.7,
        "top_p": 0.9
    }
    try:
        logger.info(f"Generiere Code mit Memory-Kontext")
        r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                   json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()
        content = data["choices"][0]["message"]["content"]
        memory.add_conversation(
            user_prompt=user_prompt,
            generated_code=content,
            system_prompt=system_prompt,
            model_used=model,
            tags=["non-streaming", "code-generation"]
        )
        return content
    except Exception as e:
        raise

def clear_cache():
    try:
        if MODELS_CACHE.exists():
            MODELS_CACHE.unlink()
            logger.info("Cache gelöscht")
    except Exception as e:
        logger.error(f"Cache löschen fehlgeschlagen: {e}")
