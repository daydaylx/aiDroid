#!/usr/bin/env python3
"""Tests für main.py"""

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test dass alle Module importiert werden können"""
    try:
        import main
        import memory
        import utils
        assert main is not None
        assert memory is not None
        assert utils is not None
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")

def test_widget_pool():
    """Test Widget Pool Funktionalität"""
    from main import WidgetPool
    
    pool = WidgetPool()
    label1 = pool.get_label()
    label2 = pool.get_label()
    
    assert label1 is not None
    assert label2 is not None
    assert label1 != label2
    
    # Return label to pool
    pool.return_label(label1)
    label3 = pool.get_label()
    
    # Should reuse the returned label
    assert label3 == label1

def test_app_initialization():
    """Test App kann initialisiert werden"""
    from main import aiDroidApp
    
    app = aiDroidApp()
    assert app.title == "aiDroid - Samsung S25 Pro"
    assert app.theme_cls.primary_palette == "DeepPurple"
    assert app.theme_cls.theme_style == "Dark"

if __name__ == "__main__":
    pytest.main([__file__])
