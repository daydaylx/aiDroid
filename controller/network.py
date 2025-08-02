import httpx
import os
import asyncio

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or ""  # alternativ in .env laden
OPENROUTER_URL = "https://openrouter.ai/api/v1"

class OpenRouterClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "aidroid.app",
            "X-Title": "aiDroid – S25"
        }

    async def fetch_models(self):
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{OPENROUTER_URL}/models", headers=self.headers)
            return res.json().get("data", [])

    async def stream(self, model, messages):
        url = f"{OPENROUTER_URL}/chat/completions"
        headers = self.headers | {"Content-Type": "application/json"}
        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "temperature": 0.7
        }
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", url, headers=headers, json=payload) as response:
                buffer = ""
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        chunk = line.removeprefix("data: ")
                        if chunk == "[DONE]":
                            break
                        try:
                            token = httpx.Response._json_decoder.decode(chunk)["choices"][0]["delta"].get("content", "")
                            if token:
                                yield token
                        except Exception:
                            continue
