#!/usr/bin/env python3
"""Tests für memory.py"""

import pytest
import os
import tempfile
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory import MemoryDB


def test_memory_db_init():
    """Test MemoryDB Initialisierung"""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = os.path.join(temp_dir, "test.db")
        db = MemoryDB(db_path)

        assert os.path.exists(db.db_path)


def test_store_and_retrieve_message():
    """Test Nachrichten speichern und abrufen"""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = os.path.join(temp_dir, "test.db")
        db = MemoryDB(db_path)

        # Store message
        msg_id = db.store_message("Test message", device_info="Samsung S25")
        assert msg_id is not None

        # Retrieve messages
        messages = db.get_recent_messages(1)
        assert len(messages) == 1
        assert "Test message" in messages[0][1]


def test_stats():
    """Test Statistiken"""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = os.path.join(temp_dir, "test.db")
        db = MemoryDB(db_path)

        # Add some data
        msg_id = db.store_message("Test", device_info="Samsung S25")
        db.store_response(msg_id, "Response", processing_time=0.5)

        stats = db.get_stats()
        assert stats["message_count"] == 1
        assert stats["response_count"] == 1
        assert stats["avg_processing_time"] == 0.5


if __name__ == "__main__":
    pytest.main([__file__])
