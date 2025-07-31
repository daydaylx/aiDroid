#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import json
import datetime
from typing import List, Tuple, Optional, Dict, Any
from kivy.utils import platform

if platform == "android":
    try:
        from jnius import autoclass

        PythonActivity = autoclass("org.kivy.android.PythonActivity")
    except ImportError:
        PythonActivity = None
else:
    PythonActivity = None


class MemoryDB:
    """Optimierte SQLite-Datenbank für Samsung S25"""

    def __init__(self, db_name: str = "aidroid_s25_memory.db"):
        self.db_name = db_name
        self.db_path = self._get_database_path()
        self._init_database()
        print(f"📁 Database: {self.db_path}")

    def _get_database_path(self) -> str:
        """Datenbankpfad ermitteln"""
        try:
            if platform == "android" and PythonActivity:
                app_dir = PythonActivity.mActivity.getFilesDir().getPath()
                return os.path.join(app_dir, self.db_name)
            else:
                return os.path.join(os.getcwd(), self.db_name)
        except Exception:
            return os.path.join(os.getcwd(), self.db_name)

    def _init_database(self) -> None:
        """Datenbank initialisieren mit Performance-Optimierungen"""
        try:
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)

            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA journal_mode=WAL")  # Performance
            conn.execute("PRAGMA synchronous=NORMAL")  # Schneller
            conn.execute("PRAGMA cache_size=10000")  # Mehr Cache
            conn.execute("PRAGMA temp_store=MEMORY")  # RAM statt Disk

            cur = conn.cursor()

            # Messages Tabelle mit Indizes
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    message_type TEXT DEFAULT 'user',
                    device_info TEXT,
                    session_id TEXT
                )
            """
            )

            # Responses Tabelle
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id INTEGER,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    processing_time REAL,
                    FOREIGN KEY (message_id) REFERENCES messages(id)
                )
            """
            )

            # Sessions Tabelle für Kontextverwaltung
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_data TEXT,
                    device_model TEXT,
                    android_version TEXT,
                    app_version TEXT DEFAULT '2.0.0',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Performance-Indizes
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)"
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_messages_type ON messages(message_type)"
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_responses_message_id ON responses(message_id)"
            )

            conn.commit()
            conn.close()

            print("✅ Database initialized with S25 optimizations")

        except Exception as e:
            print(f"❌ DB initialization error: {e}")

    def store_message(
        self,
        content: str,
        message_type: str = "user",
        device_info: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Optional[int]:
        """Nachricht speichern mit erweiterten Metadaten"""
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            # Samsung S25 Info hinzufügen
            if not device_info and platform == "android":
                try:
                    from jnius import autoclass

                    Build = autoclass("android.os.Build")
                    device_info = f"{Build.MANUFACTURER} {Build.MODEL} (Android {Build.VERSION.RELEASE})"
                except ImportError:
                    device_info = "Samsung Galaxy S25 (simulated)"

            cur.execute(
                """
                INSERT INTO messages (content, message_type, device_info, session_id) 
                VALUES (?, ?, ?, ?)
            """,
                (content, message_type, device_info, session_id),
            )

            message_id = cur.lastrowid
            conn.commit()
            conn.close()

            return message_id

        except Exception as e:
            print(f"❌ Error storing message: {e}")
            return None

    def store_response(
        self, message_id: int, content: str, processing_time: Optional[float] = None
    ) -> Optional[int]:
        """Response speichern mit Performance-Metriken"""
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO responses (message_id, content, processing_time) 
                VALUES (?, ?, ?)
            """,
                (message_id, content, processing_time),
            )

            response_id = cur.lastrowid
            conn.commit()
            conn.close()

            return response_id

        except Exception as e:
            print(f"❌ Error storing response: {e}")
            return None

    def get_recent_messages(self, limit: int = 10) -> List[Tuple]:
        """Aktuelle Nachrichten abrufen"""
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            cur.execute(
                """
                SELECT id, content, timestamp, message_type, device_info 
                FROM messages 
                ORDER BY timestamp DESC 
                LIMIT ?
            """,
                (limit,),
            )

            messages = cur.fetchall()
            conn.close()

            return messages

        except Exception as e:
            print(f"❌ Error fetching recent messages: {e}")
            return []

    def get_conversation_history(self, limit: int = 20) -> List[Tuple]:
        """Vollständige Konversationshistorie"""
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            cur.execute(
                """
                SELECT 
                    m.id, m.content, m.timestamp, m.message_type,
                    r.content as response, r.timestamp as response_time, r.processing_time
                FROM messages m
                LEFT JOIN responses r ON m.id = r.message_id
                ORDER BY m.timestamp DESC
                LIMIT ?
            """,
                (limit,),
            )

            history = cur.fetchall()
            conn.close()

            return history

        except Exception as e:
            print(f"❌ Error fetching conversation history: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """Statistiken über die Datenbank"""
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            # Message Count
            cur.execute("SELECT COUNT(*) FROM messages")
            message_count = cur.fetchone()[0]

            # Response Count
            cur.execute("SELECT COUNT(*) FROM responses")
            response_count = cur.fetchone()[0]

            # Average Processing Time
            cur.execute(
                "SELECT AVG(processing_time) FROM responses WHERE processing_time IS NOT NULL"
            )
            avg_processing_time = cur.fetchone()[0] or 0

            # Database Size
            cur.execute(
                "SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()"
            )
            db_size = cur.fetchone()[0]

            # Device Distribution
            cur.execute(
                """
                SELECT device_info, COUNT(*) as count 
                FROM messages 
                WHERE device_info IS NOT NULL 
                GROUP BY device_info
            """
            )
            device_stats = cur.fetchall()

            conn.close()

            return {
                "message_count": message_count,
                "response_count": response_count,
                "avg_processing_time": round(avg_processing_time, 3),
                "db_size_mb": round(db_size / (1024 * 1024), 2),
                "device_stats": device_stats,
            }

        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return {}

    def cleanup_old_data(self, days: int = 30) -> int:
        """Alte Daten löschen für Performance"""
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            # Alte Messages löschen
            cur.execute(
                """
                DELETE FROM messages 
                WHERE timestamp < datetime('now', '-{} days')
            """.format(
                    days
                )
            )

            deleted_messages = cur.rowcount

            # Verwaiste Responses löschen
            cur.execute(
                """
                DELETE FROM responses 
                WHERE message_id NOT IN (SELECT id FROM messages)
            """
            )

            deleted_responses = cur.rowcount

            # VACUUM für Speicheroptimierung
            cur.execute("VACUUM")

            conn.commit()
            conn.close()

            print(
                f"🧹 Cleanup: {deleted_messages} messages, {deleted_responses} responses deleted"
            )
            return deleted_messages + deleted_responses

        except Exception as e:
            print(f"❌ Cleanup error: {e}")
            return 0

    def export_data(self, filepath: str) -> bool:
        """Daten exportieren für Backup"""
        try:
            conn = sqlite3.connect(self.db_path)

            # Alle Daten als JSON exportieren
            data = {
                "messages": [],
                "responses": [],
                "export_timestamp": datetime.datetime.now().isoformat(),
            }

            # Messages exportieren
            cur = conn.cursor()
            cur.execute("SELECT * FROM messages")
            columns = [description[0] for description in cur.description]

            for row in cur.fetchall():
                data["messages"].append(dict(zip(columns, row)))

            # Responses exportieren
            cur.execute("SELECT * FROM responses")
            columns = [description[0] for description in cur.description]

            for row in cur.fetchall():
                data["responses"].append(dict(zip(columns, row)))

            conn.close()

            # JSON exportieren
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"📤 Data exported to: {filepath}")
            return True

        except Exception as e:
            print(f"❌ Export error: {e}")
            return False


if __name__ == "__main__":
    # Test-Code
    db = MemoryDB()

    # Test Message
    msg_id = db.store_message(
        "Test Message für Samsung Galaxy S25!",
        device_info="Samsung SM-S921B (Android 15)",
    )
    if msg_id:
        db.store_response(msg_id, "Test Response vom KI-System", processing_time=0.85)

    print("Recent Messages:", db.get_recent_messages(5))
    print("Stats:", db.get_stats())
