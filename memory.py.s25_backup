#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
import json
from datetime import datetime
from kivy.utils import platform

if platform == 'android':
    try:
        from jnius import autoclass, cast
        Environment = autoclass('android.os.Environment')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
    except ImportError:
        print("Android-specific modules not available")
        Environment = None
        PythonActivity = None
else:
    Environment = None
    PythonActivity = None

class MemoryDB:
    def __init__(self, db_name="aidroid_memory.db"):
        """Initialize the memory database"""
        self.db_name = db_name
        self.db_path = self._get_database_path()
        self.init_database()

    def _get_database_path(self):
        """Get platform-specific database path"""
        try:
            if platform == 'android' and PythonActivity:
                # Android: Use app's internal storage
                activity = PythonActivity.mActivity
                app_dir = activity.getFilesDir().getPath()
                db_path = os.path.join(app_dir, self.db_name)
                print(f"Android DB path: {db_path}")
                return db_path
            else:
                # Desktop: Use local directory
                db_path = os.path.join(os.getcwd(), self.db_name)
                print(f"Desktop DB path: {db_path}")
                return db_path
        except Exception as e:
            print(f"Error getting database path: {e}")
            # Fallback to current directory
            return os.path.join(os.getcwd(), self.db_name)

    def init_database(self):
        """Initialize the database with required tables"""
        try:
            # Ensure directory exists
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    message_type TEXT DEFAULT 'user'
                )
            ''')
            
            # Create responses table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id INTEGER,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (message_id) REFERENCES messages (id)
                )
            ''')
            
            # Create sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_data TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            print(f"Database initialized at: {self.db_path}")
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise

    def store_message(self, content, message_type="user"):
        """Store a message in the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO messages (content, message_type)
                VALUES (?, ?)
            ''', (content, message_type))
            
            message_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"Message stored with ID: {message_id}")
            return message_id
            
        except Exception as e:
            print(f"Error storing message: {e}")
            return None

    def store_response(self, message_id, content):
        """Store a response linked to a message"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO responses (message_id, content)
                VALUES (?, ?)
            ''', (message_id, content))
            
            response_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"Response stored with ID: {response_id}")
            return response_id
            
        except Exception as e:
            print(f"Error storing response: {e}")
            return None

    def get_recent_messages(self, limit=10):
        """Get recent messages from the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, content, timestamp, message_type
                FROM messages
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            messages = cursor.fetchall()
            conn.close()
            
            return messages
            
        except Exception as e:
            print(f"Error getting recent messages: {e}")
            return []

    def get_conversation_history(self, limit=20):
        """Get conversation history with messages and responses"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    m.id,
                    m.content as message,
                    m.timestamp as msg_time,
                    r.content as response,
                    r.timestamp as resp_time
                FROM messages m
                LEFT JOIN responses r ON m.id = r.message_id
                ORDER BY m.timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            history = cursor.fetchall()
            conn.close()
            
            return history
            
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []

    def save_session(self, session_data):
        """Save session data as JSON"""
        try:
            json_data = json.dumps(session_data)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO sessions (session_data)
                VALUES (?)
            ''', (json_data,))
            
            session_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"Session saved with ID: {session_id}")
            return session_id
            
        except Exception as e:
            print(f"Error saving session: {e}")
            return None

    def load_latest_session(self):
        """Load the latest session data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT session_data
                FROM sessions
                ORDER BY updated_at DESC
                LIMIT 1
            ''')
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return json.loads(result[0])
            return None
            
        except Exception as e:
            print(f"Error loading session: {e}")
            return None

    def clear_old_data(self, days=30):
        """Clear data older than specified days"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM messages 
                WHERE timestamp < datetime('now', '-{} days')
            '''.format(days))
            
            cursor.execute('''
                DELETE FROM responses 
                WHERE timestamp < datetime('now', '-{} days')
            '''.format(days))
            
            cursor.execute('''
                DELETE FROM sessions 
                WHERE created_at < datetime('now', '-{} days')
            '''.format(days))
            
            conn.commit()
            conn.close()
            
            print(f"Cleared data older than {days} days")
            
        except Exception as e:
            print(f"Error clearing old data: {e}")

    def get_database_info(self):
        """Get database information"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Count messages
            cursor.execute('SELECT COUNT(*) FROM messages')
            message_count = cursor.fetchone()[0]
            
            # Count responses
            cursor.execute('SELECT COUNT(*) FROM responses')
            response_count = cursor.fetchone()[0]
            
            # Count sessions
            cursor.execute('SELECT COUNT(*) FROM sessions')
            session_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'database_path': self.db_path,
                'message_count': message_count,
                'response_count': response_count,
                'session_count': session_count
            }
            
        except Exception as e:
            print(f"Error getting database info: {e}")
            return {}

if __name__ == "__main__":
    # Test the MemoryDB class
    try:
        db = MemoryDB()
        
        # Test storing a message
        msg_id = db.store_message("Test message")
        if msg_id:
            db.store_response(msg_id, "Test response")
        
        # Test getting recent messages
        messages = db.get_recent_messages(5)
        print(f"Recent messages: {messages}")
        
        # Test database info
        info = db.get_database_info()
        print(f"Database info: {info}")
        
    except Exception as e:
        print(f"Error testing MemoryDB: {e}")
EOF

