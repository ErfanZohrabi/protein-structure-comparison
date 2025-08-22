#!/usr/bin/env python3
"""
🧬 Advanced Protein Structure Viewer - Launcher Script

This script sets up and launches the complete protein analysis platform:
- Installs all dependencies 
- Starts Flask backend server with PyMMseqs integration
- Launches frontend web interface
- Provides comprehensive protein analysis capabilities

Usage: python launch.py [--dev] [--port PORT] [--no-install]
"""

import os
import sys
import subprocess
import time
import webbrowser
import argparse
from pathlib import Path
import threading

def print_banner():
    """Print application banner"""
    print("🧬" + "=" * 68 + "🧬")
    print("🧬  ADVANCED PROTEIN STRUCTURE VIEWER                            🧬")
    print("🧬  AlphaFold vs ESMFold with PyMMseqs Integration              🧬") 
    print("🧬" + "=" * 68 + "🧬")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies(force_install=False):
    """Install required dependencies"""
    
    if not force_install:
        try:
            import flask
            import requests
            import numpy
            print("✅ Core dependencies already installed")
            return True
        except ImportError:
            pass
    
    print("📦 Installing dependencies...")
    
    try:
        # Install core requirements
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Core dependencies installed successfully")
        
        # Try to install PyMMseqs (may fail on some systems)
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "pymmseqs"
            ])
            print("✅ PyMMseqs installed successfully")
        except subprocess.CalledProcessError:
            print("⚠️ PyMMseqs installation failed - advanced features will use mock data")
            print("   For full functionality, install manually: pip install pymmseqs")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_dependencies():
    """Check if all dependencies are available"""
    dependencies = {
        'flask': 'Flask web framework',
        'flask_cors': 'Flask CORS support', 
        'requests': 'HTTP requests library',
        'numpy': 'Numerical computing',
        'pandas': 'Data analysis',
        'Bio': 'Bioinformatics tools (BioPython)'
    }
    
    missing = []
    available = []
    
    for dep, desc in dependencies.items():
        try:
            __import__(dep)
            available.append(f"✅ {dep}: {desc}")
        except ImportError:
            missing.append(f"❌ {dep}: {desc}")
    
    print("📋 Dependency Status:")
    for item in available:
        print(f"   {item}")
    for item in missing:
        print(f"   {item}")
    
    # Check optional dependencies
    try:
        __import__('pymmseqs')
        print("   ✅ pymmseqs: Advanced homology search (FULL FEATURES)")
    except ImportError:
        print("   ⚠️ pymmseqs: Not available (mock data will be used)")
    
    return len(missing) == 0

def start_backend_server(port=5000, dev_mode=False):
    """Start the Flask backend server"""
    
    def run_server():
        try:
            print(f"🚀 Starting backend server on port {port}...")
            
            # Set environment variables
            os.environ['FLASK_ENV'] = 'development' if dev_mode else 'production'
            os.environ['FLASK_PORT'] = str(port)
            
            # Start Flask server
            from backend_server import app
            app.run(
                host='0.0.0.0',
                port=port,
                debug=dev_mode,
                use_reloader=False,  # Disable reloader to avoid threading issues
                threaded=True
            )
            
        except Exception as e:
            print(f"❌ Failed to start backend server: {e}")
    
    # Start server in separate thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(3)
    
    return server_thread

def open_browser(url, delay=2):
    """Open browser after a delay"""
    def delayed_open():
        time.sleep(delay)
        try:
            webbrowser.open(url)
            print(f"🌐 Browser opened to: {url}")
        except Exception as e:
            print(f"⚠️ Could not open browser: {e}")
            print(f"   Please manually navigate to: {url}")
    
    browser_thread = threading.Thread(target=delayed_open, daemon=True)
    browser_thread.start()
    return browser_thread

def check_server_health(url, max_retries=10):
    """Check if server is responding"""
    import requests
    
    for i in range(max_retries):
        try:
            response = requests.get(f"{url}/api/status", timeout=5)
            if response.status_code == 200:
                return True
        except:
            pass
        
        if i < max_retries - 1:
            print(f"⏳ Waiting for server... ({i+1}/{max_retries})")
            time.sleep(1)
    
    return False

def display_feature_summary():
    """Display available features"""
    print("\n🌟 FEATURES AVAILABLE:")
    print("   🔍 Protein Search: UniProt ID lookup with auto-suggestions")
    print("   🧬 3D Visualization: PyMOL-style dual viewers (AlphaFold vs ESMFold)")
    print("   📊 Advanced Analysis: Homology search with PyMMseqs integration")
    print("   🧬 Evolutionary Analysis: Conservation scoring and phylogenetic depth")
    print("   📈 Interactive Plots: Real-time structure comparison visualizations")
    print("   📱 Responsive Design: Works on desktop, tablet, and mobile")
    print("   💾 Export Functions: Download analysis data and reports")
    print("   ⌨️ Keyboard Shortcuts: Power-user navigation")

def display_usage_instructions(url):
    """Display usage instructions"""
    print(f"\n🎯 QUICK START:")
    print(f"   1. Open your browser to: {url}")
    print(f"   2. Enter a UniProt ID (try: P01308, P61626, P68871)")
    print(f"   3. Explore 3D structures and analysis results")
    print(f"   4. Use viewer controls: Cartoon, Surface, Sticks")
    print(f"   5. Check advanced analysis panel for homology data")
    
    print(f"\n🎮 CONTROLS:")
    print(f"   • Ctrl/Cmd + K: Quick search")
    print(f"   • Mouse: Rotate, zoom, pan in 3D viewers")
    print(f"   • Reset buttons: Return to default view")
    print(f"   • Export: Download analysis data")

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(description='Launch Advanced Protein Structure Viewer')
    parser.add_argument('--dev', action='store_true', help='Run in development mode')
    parser.add_argument('--port', type=int, default=5000, help='Backend server port')
    parser.add_argument('--no-install', action='store_true', help='Skip dependency installation')
    parser.add_argument('--no-browser', action='store_true', help='Don\'t open browser automatically')
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Install dependencies
    if not args.no_install:
        if not install_dependencies():
            return 1
    
    # Check dependencies
    print("\n📋 Checking Dependencies...")
    if not check_dependencies():
        print("\n❌ Some dependencies are missing.")
        print("   Run: python launch.py (without --no-install)")
        return 1
    
    # Display features
    display_feature_summary()
    
    # Start backend server
    print(f"\n🚀 Starting Advanced Protein Analysis Platform...")
    server_thread = start_backend_server(args.port, args.dev)
    
    # Check server health
    server_url = f"http://localhost:{args.port}"
    print(f"⏳ Checking server health...")
    
    if check_server_health(server_url):
        print(f"✅ Backend server is running at: {server_url}")
        print(f"✅ Frontend interface available at: {server_url}")
        print(f"✅ API endpoints available at: {server_url}/api")
        
        # Open browser
        if not args.no_browser:
            open_browser(server_url)
        
        # Display usage instructions
        display_usage_instructions(server_url)
        
        print(f"\n🔄 Server is running... Press Ctrl+C to stop")
        print("=" * 70)
        
        try:
            # Keep main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n\n👋 Shutting down server...")
            print("Thank you for using Advanced Protein Structure Viewer!")
            return 0
    
    else:
        print(f"❌ Server failed to start properly")
        print("   Check console output for errors")
        return 1

if __name__ == "__main__":
    sys.exit(main())