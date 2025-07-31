#!/usr/bin/env python3
"""Tests für utils.py"""

import pytest
import asyncio
import tempfile
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import AsyncNetworkHandler, SecureConfigManager

def test_network_handler_init():
    """Test AsyncNetworkHandler Initialisierung"""
    handler = AsyncNetworkHandler()
    assert handler.session is not None
    assert handler.timeout == 30
    assert 'Samsung' in handler.session.headers['User-Agent']

@pytest.mark.asyncio
async def test_async_processing():
    """Test asynchrone Nachrichtenverarbeitung"""
    handler = AsyncNetworkHandler()
    
    response = await handler.process_request_async("Hello Samsung S25")
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0

def test_cache_functionality():
    """Test Caching-Funktionalität"""
    with tempfile.TemporaryDirectory() as temp_dir:
        handler = AsyncNetworkHandler()
        handler.cache_dir = temp_dir
        
        # Cache response
        message = "Test message"
        response = "Test response"
        handler.cache_response(message, response)
        
        # Retrieve cached response
        cached = handler.get_cached_response(message)
        assert cached == response

def test_config_manager():
    """Test SecureConfigManager"""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_manager = SecureConfigManager()
        config_manager.config_dir = temp_dir
        config_manager.config_file = os.path.join(temp_dir, "config.json")
        
        # Test set/get
        config_manager.set('test_key', 'test_value')
        assert config_manager.get('test_key') == 'test_value'
        
        # Test S25 optimization
        config_manager.optimize_for_s25()
        assert config_manager.get('device_optimization') == 'samsung_s25'

if __name__ == "__main__":
    pytest.main([__file__])
