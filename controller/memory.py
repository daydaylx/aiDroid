import sqlite3
from collections import deque
import time

class MemoryController:
    """
    Manages the application's memory and chat history using a SQLite database.
    This class handles the storage and retrieval of conversation data.
    """
    def __init__(self, db_path='history.db', max_history=100):
        self.db_path = db_path
        self.max_history = max_history
        self.connection = self.get_db_connection()
        self.cursor = self.connection.cursor()
        self.setup_database()
        self.conversation_deque = self.load_recent_history()

    def get_db_connection(self):
        """Creates and returns a connection to the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        return conn

    def setup_database(self):
        """
        Creates the 'messages' table if it does not exist.
        The table stores the timestamp, sender, and content of each message.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                timestamp REAL,
                sender TEXT,
                content TEXT
            )
        ''')
        self.connection.commit()

    def add_message(self, sender, content):
        """Adds a new message to the database and the in-memory deque."""
        timestamp = time.time()
        self.cursor.execute(
            "INSERT INTO messages (timestamp, sender, content) VALUES (?, ?, ?)",
            (timestamp, sender, content)
        )
        self.connection.commit()
        # Add to deque and maintain max size
        self.conversation_deque.append((timestamp, sender, content))
        if len(self.conversation_deque) > self.max_history:
            self.conversation_deque.popleft()

    def load_recent_history(self):
        """
        Loads the most recent messages from the database into the deque.
        """
        self.cursor.execute(
            "SELECT timestamp, sender, content FROM messages ORDER BY timestamp DESC LIMIT ?",
            (self.max_history,)
        )
        recent_history = self.cursor.fetchall()
        # The deque is populated in chronological order (oldest first)
        return deque(reversed(recent_history), maxlen=self.max_history)

    def get_full_history(self):
        """
        Returns all messages currently stored in the in-memory deque.
        """
        return list(self.conversation_deque)

    def close(self):
        """Closes the database connection."""
        self.connection.close()

if __name__ == '__main__':
    # Example usage:
    memory = MemoryController()
    memory.add_message("user", "Hallo, wie geht es dir?")
    memory.add_message("ai", "Mir geht es gut, danke!")
    history = memory.get_full_history()
    for message in history:
        print(f"Timestamp: {message[0]}, Sender: {message[1]}, Content: {message[2]}")
    memory.close()
