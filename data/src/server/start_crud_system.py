#!/usr/bin/env python3
"""
Start CRUD System for Retail Tariff Data
Generates data, creates CRUD viewer, and starts the server
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import flask
        import flask_cors
        print("✅ Flask dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("💡 Install with: pip install -r requirements.txt")
        return False

def main():
    """Main function to start the CRUD system"""
    print("🚀 Starting Retail Tariff Data CRUD System")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install dependencies first:")
        print("   pip install -r requirements.txt")
        return False
    
    # Generate synthetic data
    if not run_command('python3 "src/data_generation/Generate synthetic datasets for tariff.py"', "Generating synthetic datasets"):
        print("❌ Data generation failed")
        return False
    
    # Generate CRUD HTML viewer
    if not run_command("python3 src/viewers/generate_crud_html_viewer.py", "Generating CRUD HTML viewer"):
        print("❌ CRUD viewer generation failed")
        return False
    
    print("\n🎉 CRUD System Setup Complete!")
    print("📋 Generated files:")
    print("   • retail_tariff_data/ - CSV data files")
    print("   • data_viewer_crud.html - CRUD-enabled viewer")
    print("   • crud_server.py - Backend API server")
    
    print("\n🌐 Starting CRUD Server...")
    print("📊 Features available:")
    print("   • Create new rows")
    print("   • Edit existing rows")
    print("   • Delete rows")
    print("   • Data validation")
    print("   • Real-time CSV updates")
    print("   • Filtering and export")
    
    # Start the CRUD server
    try:
        print(f"\n🚀 Starting CRUD server on http://localhost:5001")
        print("💡 Press Ctrl+C to stop the server")
        
        # Start server in background
        server_process = subprocess.Popen([
            sys.executable, "src/server/crud_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Open browser
        try:
            webbrowser.open("http://localhost:5001")
            print("🌐 CRUD viewer opened in your browser")
        except Exception as e:
            print(f"❌ Failed to open browser: {e}")
            print("💡 Please open http://localhost:5001 manually")
        
        # Keep server running
        try:
            server_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down CRUD server...")
            server_process.terminate()
            server_process.wait()
            print("✅ Server stopped")
            
    except Exception as e:
        print(f"❌ Failed to start CRUD server: {e}")
        print("💡 Manual start: python3 src/server/crud_server.py")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
