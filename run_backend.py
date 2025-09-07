#!/usr/bin/env python3
"""
Backend Runner Script
Starts the Flask backend server with proper configuration
"""

import os
import sys
from dotenv import load_dotenv

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

# Load environment variables
load_dotenv()

# Import and run the Flask app
from app import app

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"🚀 Starting Auto Feedback Generator Backend")
    print(f"📍 Server: http://localhost:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"🤖 OpenAI API configured: {bool(os.getenv('OPENAI_API_KEY'))}")
    print("-" * 50)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )