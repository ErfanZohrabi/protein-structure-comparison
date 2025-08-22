#!/usr/bin/env python3
"""
Simple HTTP Server for Protein Structure Viewer Website

This script starts a local web server to serve the protein visualization website.
It handles CORS headers to allow API requests and provides a better development experience.
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP Request Handler with CORS support"""
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle preflight CORS requests"""
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        """Custom logging to show protein viewer specific messages"""
        message = format % args
        if 'GET' in message and any(ext in message for ext in ['.html', '.js', '.css']):
            print(f"🌐 Serving: {message}")
        elif 'GET' in message:
            print(f"📡 Request: {message}")

def start_server(port=8000):
    """Start the protein viewer web server"""
    
    # Change to the website directory
    website_dir = Path(__file__).parent
    os.chdir(website_dir)
    
    print("🧬 Protein Structure Viewer - Web Server")
    print("=" * 50)
    print(f"📁 Serving from: {website_dir.absolute()}")
    print(f"🌐 Port: {port}")
    
    # Check if required files exist
    required_files = ['index.html', 'js/app.js', 'js/site.js', 'css/styles.css']
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please ensure all website files are present")
        return
    
    try:
        # Create server
        with socketserver.TCPServer(("", port), CORSHTTPRequestHandler) as httpd:
            server_url = f"http://localhost:{port}"
            
            print(f"✅ Server started successfully!")
            print(f"🔗 URL: {server_url}")
            print("\n🚀 Features available:")
            print("  • Protein search by UniProt ID")
            print("  • 3D PyMOL-style visualization")
            print("  • AlphaFold vs ESMFold comparison")
            print("  • Interactive molecular viewers")
            print("  • Real-time protein information")
            print("\n📚 Example proteins to try:")
            print("  • P01308 - Human Insulin")
            print("  • P61626 - Lysozyme")
            print("  • P68871 - Hemoglobin")
            print("\n🎮 Controls:")
            print("  • Ctrl/Cmd + K: Quick search")
            print("  • Arrow keys: Navigate suggestions")
            print("  • Escape: Clear search")
            
            print(f"\n🌐 Opening browser...")
            
            # Open browser
            try:
                webbrowser.open(server_url)
                print(f"✅ Browser opened to {server_url}")
            except Exception as e:
                print(f"⚠️ Could not open browser: {e}")
                print(f"Please manually navigate to: {server_url}")
            
            print(f"\n🔄 Server is running... Press Ctrl+C to stop")
            print("=" * 50)
            
            # Start serving
            httpd.serve_forever()
            
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use")
            print(f"🔄 Trying port {port + 1}...")
            start_server(port + 1)
        else:
            print(f"❌ Server error: {e}")
    except KeyboardInterrupt:
        print(f"\n\n👋 Server stopped by user")
        print("Thank you for using Protein Structure Viewer!")

def main():
    """Main function with command line argument handling"""
    
    # Default port
    port = 8000
    
    # Check for port argument
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
            if not (1024 <= port <= 65535):
                raise ValueError("Port must be between 1024 and 65535")
        except ValueError as e:
            print(f"❌ Invalid port: {e}")
            print("Usage: python server.py [port]")
            print("Example: python server.py 8080")
            return
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required")
        return
    
    # Start the server
    start_server(port)

if __name__ == "__main__":
    main()