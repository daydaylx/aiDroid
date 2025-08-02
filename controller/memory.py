from collections import deque
from time import time

class MessageContext:
    """
    Speichert Chatverlauf für OpenRouter-kompatible Anfragen.
    Kann später um Tokenbegrenzung oder automatische Zusammenfassung erweitert werden.
    """
    def __init__(self, max_messages=20):
        self.history = deque(maxlen=max_messages)
        self.current_ai_msg = []

    def add(self, role, content):
        self.history.append({"role": role, "content": content})

    def get(self):
        return list(self.history) + ([{"role": "assistant", "content": ""}] if self.current_ai_msg else [])

    def finalize(self, role):
        if role == "ai" and self.current_ai_msg:
            full = "".join(self.current_ai_msg)
            self.add("assistant", full)
            self.current_ai_msg.clear()

    def stream_token(self, token):
        self.current_ai_msg.append(token)

    def clear(self):
        self.history.clear()
        self.current_ai_msg.clear()
