#!/usr/bin/env python3
import http.server
import socketserver
import os
import threading
import time
import subprocess
import socket
from pathlib import Path

class HotReloadHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="/Users/dylan/Desktop/pseo/clean_site", **kwargs)
    
    def end_headers(self):
        # Add hot reload script and CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def do_GET(self):
        # Handle clean URLs (no .html extension)
        if self.path.endswith('/') and self.path != '/':
            # Remove trailing slash and redirect
            self.send_response(301)
            self.send_header('Location', self.path[:-1])
            self.end_headers()
            return
        
        # If path doesn't have extension and isn't root, look for directory with index.html
        if '.' not in os.path.basename(self.path) and self.path != '/':
            # Try to serve from directory/index.html
            test_path = os.path.join(self.directory, self.path.lstrip('/'), 'index.html')
            if os.path.exists(test_path):
                self.path = f"{self.path}/index.html"
        
        # Add hot reload script to HTML responses
        super().do_GET()
    
    def do_POST(self):
        # Handle POST requests (for hot reload)
        if self.path == '/reload':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            super().do_POST()

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote server to get local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "localhost"

def watch_files():
    """Watch for file changes and trigger reload"""
    import time
    import os
    
    site_dir = "/Users/dylan/Desktop/pseo/clean_site"
    last_modified = {}
    
    def get_file_times(directory):
        times = {}
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(('.html', '.css', '.js')):
                    filepath = os.path.join(root, file)
                    times[filepath] = os.path.getmtime(filepath)
        return times
    
    print("🔍 Watching for file changes...")
    last_modified = get_file_times(site_dir)
    
    while True:
        time.sleep(1)
        current_times = get_file_times(site_dir)
        
        for filepath, mtime in current_times.items():
            if filepath not in last_modified or last_modified[filepath] != mtime:
                print(f"📝 File changed: {os.path.basename(filepath)}")
                last_modified = current_times
                break

def start_server():
    """Start the HTTP server"""
    PORT = 8080
    local_ip = get_local_ip()
    
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), HotReloadHTTPRequestHandler) as httpd:
            print("🚀 Local Pet Grooming Dev Server Starting...")
            print("=" * 60)
            print(f"🌐 Local: http://localhost:{PORT}")
            print(f"📱 Network: http://{local_ip}:{PORT}")
            print("=" * 60)
            print("📋 Available Pages:")
            print(f"   • Homepage: http://{local_ip}:{PORT}/")
            print(f"   • Austin: http://{local_ip}:{PORT}/austin")
            print(f"   • Miami: http://{local_ip}:{PORT}/miami")
            print(f"   • Privacy: http://{local_ip}:{PORT}/privacy")
            print(f"   • Terms: http://{local_ip}:{PORT}/terms")
            print("=" * 60)
            print("🔥 Hot reload enabled - files will auto-refresh!")
            print("⏹️  Press Ctrl+C to stop server")
            print("=" * 60)
            
            # Start file watcher in background thread
            watcher_thread = threading.Thread(target=watch_files, daemon=True)
            watcher_thread.start()
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use. Trying port 8081...")
            try:
                with socketserver.TCPServer(("0.0.0.0", 8081), HotReloadHTTPRequestHandler) as httpd:
                    print(f"🌐 Server running on http://{local_ip}:8081")
                    httpd.serve_forever()
            except Exception as e:
                print(f"❌ Error starting server: {e}")
        else:
            print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    start_server()