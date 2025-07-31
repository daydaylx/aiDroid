#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import json
from kivy.utils import platform

if platform == 'android':
    try:
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
    except ImportError:
        PythonActivity = None
else:
    PythonActivity = None

class MemoryDB:
    def __init__(self, db_name="aidroid_memory.db"):
        self.db_name = db_name
        self.db_path = self._get_database_path()
        self._init_database()

    def _get_database_path(self):
        try:
            if platform == 'android' and PythonActivity:
                app_dir = PythonActivity.mActivity.getFilesDir().getPath()
                return os.path.join(app_dir, self.db_name)
            else:
                return os.path.join(os.getcwd(), self.db_name)
        except Exception:
            return os.path.join(os.getcwd(), self.db_name)

    def _init_database(self):
        try:
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)

            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    message_type TEXT DEFAULT 'user'
                )
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id INTEGER,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (message_id) REFERENCES messages(id)
                )
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_data TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"DB initialization error: {e}")

    def store_message(self, content, message_type="user"):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute('INSERT INTO messages (content, message_type) VALUES (?, ?)', (content, message_type))
            message_id = cur.lastrowid
            conn.commit()
            conn.close()
            return message_id
        except Exception as e:
            print(f"Error storing message: {e}")
            return None

    def store_response(self, message_id, content):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute('INSERT INTO responses (message_id, content) VALUES (?, ?)', (message_id, content))
            response_id = cur.lastrowid
            conn.commit()
            conn.close()
            return response_id
        except Exception as e:
            print(f"Error storing response: {e}")
            return None

    def get_recent_messages(self, limit=10):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute('SELECT id, content, timestamp, message_type FROM messages ORDER BY timestamp DESC LIMIT ?', (limit,))
            messages = cur.fetchall()
            conn.close()
            return messages
        except Exception as e:
            print(f"Error fetching recent messages: {e}")
            return []

    def get_conversation_history(self, limit=20):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute('''
                SELECT 
                    m.id, m.content, m.timestamp,
                    r.content, r.timestamp
                FROM messages m
                LEFT JOIN responses r ON m.id = r.message_id
                ORDER BY m.timestamp DESC
                LIMIT ?
                ''', (limit,))
            history = cur.fetchall()
            conn.close()
            return history
        except Exception as e:
            print(f"Error fetching conversation history: {e}")
            return []

if __name__ == "__main__":
    db = MemoryDB()
    msg_id = db.store_message("Hallo vom Galaxy S25!")
    if msg_id:
        db.store_response(msg_id, "Willkommen bei aiDroid auf deinem S25!")
    print(db.get_recent_messages(5))
