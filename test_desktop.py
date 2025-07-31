#!/usr/bin/env python3
"""Desktop test for aiDroid"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main import aiDroidApp

    print("✅ Importing main.py successful")

    print("🖥️  Starting desktop test...")
    app = aiDroidApp()
    app.run()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install requirements: pip install kivy kivymd")
    sys.exit(1)

except Exception as e:
    print(f"❌ Runtime error: {e}")
    sys.exit(1)
