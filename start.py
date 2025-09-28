#!/usr/bin/env python3
"""
Startup script for TariffTok AI.
"""

import sys
import os
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed."""
    try:
        import fastapi
        import pandas
        import pydantic
        import openai
        import langgraph
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if environment file exists."""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  No .env file found!")
        print("\n📋 To set up your environment:")
        print("1. Copy the example configuration:")
        print("   cp config/env/env.example .env")
        print("\n2. Edit .env with your Azure OpenAI credentials:")
        print("   - AZURE_OPENAI_API_KEY")
        print("   - AZURE_OPENAI_ENDPOINT")
        print("   - AZURE_OPENAI_DEPLOYMENT_NAME")
        return False
    return True

def check_data_files():
    """Check if data files exist."""
    data_path = Path("data/retail_tariff_data")
    required_files = ["tariffs.csv", "products.csv", "suppliers.csv"]
    
    missing_files = []
    for file in required_files:
        if not (data_path / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing data files: {missing_files}")
        return False
    
    print("✅ Data files found")
    return True

def start_server():
    """Start the FastAPI server."""
    print("\n🚀 Starting TariffTok AI...")
    print("=" * 50)
    
    try:
        # Import and run the main module
        from src.main import app
        import uvicorn
        
        print("🌐 Server starting at http://localhost:8080")
        print("📱 Open your browser to start asking about tariffs!")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        uvicorn.run(
            "src.main:app",
            host="0.0.0.0",
            port=8080,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

def main():
    """Main startup function."""
    print("🏭 TariffTok AI - Tariff Analysis System")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment file
    if not check_env_file():
        sys.exit(1)
    
    # Check data files
    if not check_data_files():
        sys.exit(1)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
