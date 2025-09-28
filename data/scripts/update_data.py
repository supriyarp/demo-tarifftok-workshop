#!/usr/bin/env python3
"""
Retail Tariff Data Update Script
Automatically regenerates all data and updates the HTML viewer
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def check_dependencies():
    """Check if required packages are available"""
    print("📦 Checking Python dependencies...")
    try:
        import pandas
        import numpy
        print("✅ All dependencies are available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Installing required packages...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pandas", "numpy"], check=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False

def show_data_summary():
    """Show summary of generated data"""
    print("\n📈 Data Summary:")
    print("=" * 50)
    
    data_dir = Path("retail_tariff_data")
    if data_dir.exists():
        csv_files = list(data_dir.glob("*.csv"))
        if csv_files:
            print("CSV Files:")
            total_size = 0
            for file in csv_files:
                size = file.stat().st_size
                total_size += size
                print(f"  {file.name} ({size:,} bytes)")
            
            print(f"\nTotal size: {total_size:,} bytes")
            
            # Count total records
            total_records = 0
            for file in csv_files:
                try:
                    with open(file, 'r') as f:
                        lines = sum(1 for line in f) - 1  # Subtract header
                        total_records += lines
                except:
                    pass
            
            print(f"Total records: {total_records:,}")
        else:
            print("❌ No CSV files found")
    else:
        print("❌ Data directory not found")

def main():
    """Main update process"""
    print("🚀 Starting data update process...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Cannot proceed without required dependencies")
        sys.exit(1)
    
    # Generate synthetic data
    if not run_command('python3 "../src/data_generation/Generate synthetic datasets for tariff.py"', "Generating synthetic datasets"):
        print("❌ Data generation failed")
        sys.exit(1)
    
    # Generate HTML viewer
    if not run_command("python3 ../src/viewers/generate_dynamic_html_viewer.py", "Generating dynamic HTML viewer"):
        print("❌ Dynamic HTML viewer generation failed")
        sys.exit(1)
    
    # Show summary
    show_data_summary()
    
    print("\n🎉 Update completed successfully!")
    print("💡 Dynamic HTML viewer generated: data_viewer_dynamic.html")
    
    # Try to open the dynamic HTML file with web server
    html_file = Path("data_viewer_dynamic.html")
    if html_file.exists():
        try:
            # Start web server in background
            print("🚀 Starting web server for dynamic viewer...")
            if sys.platform == "win32":  # Windows
                subprocess.Popen(["python", "-m", "http.server", "5200"], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:  # macOS/Linux
                subprocess.Popen(["python3", "-m", "http.server", "5200"], 
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Wait a moment for server to start
            import time
            time.sleep(2)
            
            # Open browser to localhost
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", "http://localhost:5002/data_viewer_dynamic.html"])
            elif sys.platform == "win32":  # Windows
                subprocess.run(["start", "http://localhost:5002/data_viewer_dynamic.html"], shell=True)
            else:  # Linux
                subprocess.run(["xdg-open", "http://localhost:5002/data_viewer_dynamic.html"])
            
            print("🌐 Dynamic HTML viewer opened at http://localhost:5002/data_viewer_dynamic.html")
            print("💡 Web server running on port 5002. Press Ctrl+C to stop.")
            
        except Exception as e:
            print(f"❌ Failed to start web server: {e}")
            print("💡 Manual options:")
            print("   1. Run: python3 start_web_server.py")
            print("   2. Or run: python3 -m http.server 5002")
            print("   3. Open: http://localhost:5002/data_viewer_dynamic.html")

if __name__ == "__main__":
    main()
