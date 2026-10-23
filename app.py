
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            response = {
                "status": "healthy",
                "service": "AutoHeal Demo App",
                "timestamp": datetime.now().isoformat()
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "not_found",
                "message": "Endpoint not found"
            }).encode())

    def log_message(self, format, *args):
        print(f"[APP] {self.address_string()} - {args[0]}", flush=True)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), HealthHandler)
    print("AutoHeal Demo App is running on port 8000", flush=True)
    print("Health endpoint: http://localhost:8000/health", flush=True)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping AutoHeal Demo App...", flush=True)
        server.server_close()
