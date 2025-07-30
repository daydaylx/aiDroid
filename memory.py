import sqlite3
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import logging

logger = logging.getLogger("memory")

class ConversationMemory:
    def __init__(self, db_path: str = None):
        if db_path is None:
            cache_dir = Path.home() / ".cache" / "openrouter"
            cache_dir.mkdir(parents=True, exist_ok=True)
            db_path = cache_dir / "conversation_memory.db"
        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        self.conn.executescript('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_prompt TEXT NOT NULL,
                system_prompt TEXT,
                model_used TEXT,
                generated_code TEXT,
                code_hash TEXT,
                project_context TEXT,
                tags TEXT
            );
            CREATE TABLE IF NOT EXISTS project_contexts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT UNIQUE NOT NULL,
                context_data TEXT NOT NULL,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS code_snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT NOT NULL,
                description TEXT,
                language TEXT DEFAULT 'python',
                tags TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                used_count INTEGER DEFAULT 0
            );
            CREATE INDEX IF NOT EXISTS idx_session_timestamp ON conversations(session_id, timestamp);
            CREATE INDEX IF NOT EXISTS idx_code_hash ON conversations(code_hash);
            CREATE INDEX IF NOT EXISTS idx_project_context ON conversations(project_context);
        ''')
        self.conn.commit()

    def add_conversation(self, user_prompt: str, generated_code: str, 
                        system_prompt: str = "", model_used: str = "", 
                        project_context: str = "", tags: List[str] = None) -> int:
        session_id = self._get_current_session_id()
        code_hash = hashlib.md5(generated_code.encode()).hexdigest()
        tags_str = json.dumps(tags or [])
        cursor = self.conn.execute('''
            INSERT INTO conversations 
            (session_id, user_prompt, system_prompt, model_used, generated_code, 
             code_hash, project_context, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, user_prompt, system_prompt, model_used, 
              generated_code, code_hash, project_context, tags_str))
        self.conn.commit()
        return cursor.lastrowid

    def get_recent_conversations(self, limit: int = 10, project_context: str = None) -> List[Dict]:
        query = '''
            SELECT * FROM conversations 
            WHERE (? IS NULL OR project_context = ?)
            ORDER BY timestamp DESC 
            LIMIT ?
        '''
        rows = self.conn.execute(query, (project_context, project_context, limit)).fetchall()
        conversations = []
        for row in rows:
            conv = dict(row)
            conv['tags'] = json.loads(conv['tags'] or '[]')
            conversations.append(conv)
        return conversations

    def get_conversation_context(self, last_n: int = 3) -> str:
        conversations = self.get_recent_conversations(last_n)
        if not conversations:
            return ""
        context_parts = []
        for i, conv in enumerate(reversed(conversations)):
            context_parts.append(f"""\
Konversation {i+1}:
User: {conv['user_prompt'][:200]}{'...' if len(conv['user_prompt']) > 200 else ''}
Generated: {conv['generated_code'][:300]}{'...' if len(conv['generated_code']) > 300 else ''}
Model: {conv['model_used']}
""")
        return "=== KONTEXT AUS VORHERIGEN GESPRÄCHEN ===\n" + "\n".join(context_parts) + "\n=== ENDE KONTEXT ==="

    def find_similar_conversations(self, query: str, limit: int = 5) -> List[Dict]:
        keywords = query.lower().split()
        conversations = self.get_recent_conversations(50)
        scored_conversations = []
        for conv in conversations:
            score = 0
            text = (conv['user_prompt'] + ' ' + conv['generated_code']).lower()
            for keyword in keywords:
                score += text.count(keyword)
            if score > 0:
                scored_conversations.append((score, conv))
        scored_conversations.sort(reverse=True, key=lambda x: x[0])
        return [conv for score, conv in scored_conversations[:limit]]

    def save_project_context(self, project_name: str, context_data: Dict):
        context_json = json.dumps(context_data, indent=2)
        self.conn.execute('''
            INSERT OR REPLACE INTO project_contexts (project_name, context_data)
            VALUES (?, ?)
        ''', (project_name, context_json))
        self.conn.commit()

    def get_project_context(self, project_name: str) -> Optional[Dict]:
        row = self.conn.execute(
            'SELECT context_data FROM project_contexts WHERE project_name = ?',
            (project_name,)
        ).fetchone()
        if row:
            return json.loads(row['context_data'])
        return None

    def save_code_snippet(self, name: str, code: str, description: str = "", 
                         language: str = "python", tags: List[str] = None):
        tags_str = json.dumps(tags or [])
        self.conn.execute('''
            INSERT INTO code_snippets (name, code, description, language, tags)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, code, description, language, tags_str))
        self.conn.commit()

    def get_code_snippets(self, language: str = None, tag: str = None) -> List[Dict]:
        query = 'SELECT * FROM code_snippets WHERE 1=1'
        params = []
        if language:
            query += ' AND language = ?'
            params.append(language)
        if tag:
            query += ' AND tags LIKE ?'
            params.append(f'%"{tag}"%')
        query += ' ORDER BY used_count DESC, created_at DESC'
        rows = self.conn.execute(query, params).fetchall()
        snippets = []
        for row in rows:
            snippet = dict(row)
            snippet['tags'] = json.loads(snippet['tags'] or '[]')
            snippets.append(snippet)
        return snippets

    def increment_snippet_usage(self, snippet_id: int):
        self.conn.execute(
            'UPDATE code_snippets SET used_count = used_count + 1 WHERE id = ?',
            (snippet_id,)
        )
        self.conn.commit()

    def _get_current_session_id(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

    def cleanup_old_conversations(self, days_to_keep: int = 30):
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        deleted = self.conn.execute(
            'DELETE FROM conversations WHERE timestamp < ?',
            (cutoff_date,)
        ).rowcount
        self.conn.commit()
        return deleted

    def get_statistics(self) -> Dict:
        stats = {}
        row = self.conn.execute('SELECT COUNT(*) as count FROM conversations').fetchone()
        stats['total_conversations'] = row['count']
        row = self.conn.execute('SELECT COUNT(*) as count FROM code_snippets').fetchone()
        stats['total_snippets'] = row['count']
        row = self.conn.execute('SELECT COUNT(*) as count FROM project_contexts').fetchone()
        stats['total_projects'] = row['count']
        today = datetime.now().strftime("%Y-%m-%d")
        row = self.conn.execute(
            'SELECT COUNT(*) as count FROM conversations WHERE DATE(timestamp) = ?',
            (today,)
        ).fetchone()
        stats['conversations_today'] = row['count']
        return stats

    def close(self):
        self.conn.close()

memory = ConversationMemory()
