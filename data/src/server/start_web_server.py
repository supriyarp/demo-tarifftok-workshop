#!/usr/bin/env python3
"""
Start web server for dynamic HTML viewer
"""
import subprocess
import sys
import webbrowser
import time
from pathlib import Path

def start_web_server():
    """Start web server and open dynamic viewer"""
    print("🚀 Starting web server for dynamic HTML viewer...")
    
    # Check if dynamic viewer exists
    if not Path("data_viewer_dynamic.html").exists():
        print("❌ data_viewer_dynamic.html not found!")
        print("💡 Run: python3 src/viewers/generate_dynamic_html_viewer.py")
        return
    
    try:
        # Start web server
        if sys.platform == "win32":  # Windows
            server_process = subprocess.Popen(
                ["python", "-m", "http.server", "5002"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:  # macOS/Linux
            server_process = subprocess.Popen(
                ["python3", "-m", "http.server", "5002"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
        # Wait for server to start
        print("⏳ Starting server...")
        time.sleep(2)
        
        # Open browser
        url = "http://localhost:5002/data_viewer_dynamic.html"
        print(f"🌐 Opening {url}")
        webbrowser.open(url)
        
        print("✅ Web server started successfully!")
        print("📊 Dynamic viewer should now load CSV data properly")
        print("💡 Press Ctrl+C to stop the server")
        
        # Keep server running
        try:
            server_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping web server...")
            server_process.terminate()
            print("✅ Web server stopped")
            
    except Exception as e:
        print(f"❌ Failed to start web server: {e}")
        print("💡 Manual steps:")
        print("   1. Run: python3 -m http.server 5002")
        print("   2. Open: http://localhost:5002/data_viewer_dynamic.html")
        print("   3. Or use: data_viewer_crud.html (CRUD interface)")

if __name__ == "__main__":
    start_web_server()
