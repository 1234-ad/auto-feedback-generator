#!/usr/bin/env python3
"""
Frontend Runner Script
Starts the Streamlit frontend application
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Run the Streamlit frontend"""
    
    # Add frontend directory to Python path
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    sys.path.insert(0, frontend_dir)
    
    # Set environment variables for Streamlit
    os.environ['STREAMLIT_SERVER_PORT'] = os.getenv('STREAMLIT_PORT', '8501')
    os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
    
    print(f"🎓 Starting Auto Feedback Generator Frontend")
    print(f"📍 Server: http://localhost:{os.environ['STREAMLIT_SERVER_PORT']}")
    print(f"🔗 Backend URL: {os.getenv('BACKEND_URL', 'http://localhost:5000')}")
    print("-" * 50)
    
    # Run Streamlit
    app_path = os.path.join(frontend_dir, 'app.py')
    
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', app_path,
            '--server.port', os.environ['STREAMLIT_SERVER_PORT'],
            '--server.address', os.environ['STREAMLIT_SERVER_ADDRESS'],
            '--server.headless', 'true' if os.getenv('STREAMLIT_HEADLESS') == 'true' else 'false'
        ])
    except KeyboardInterrupt:
        print("\\n👋 Frontend server stopped")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()