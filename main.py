import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pyrogram import Client, filters

# --- DUMMY WEB SERVER FOR RENDER (Nidrapokunda undadaniki) ---
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is active & running seamlessly!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()
# -----------------------------------

# Settings reading from Render Environment Variables
SESSION = os.environ.get("SESSION")
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH")

def get_channels(env_var):
    data = os.environ.get(env_var, "")
    if not data: return []
    channels = []
    for x in data.split(","):
        x = x.strip().replace("@", "")
        if not x: continue
        try:
            channels.append(int(x)) # -100 tho unna IDs kosam
        except ValueError:
            channels.append(x) # Usernames kosam
        return channels

# Permanent lists
SOURCES = get_channels("SOURCES")
DESTINATIONS = get_channels("DESTINATIONS")

app = Client("forwarding_bot", session_string=SESSION, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.chat(SOURCES))
def forwarder(client, message):
    for dest in DESTINATIONS:
        try:
            message.forward(dest)
        except Exception as e:
            print(f"Error sending to {dest}: {e}")

print("Bot is successfully starting...")
app.run()
