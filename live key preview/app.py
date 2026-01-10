import threading
from flask import Flask, render_template
from pynput import keyboard

app = Flask(__name__)


last_key = "Waiting..."

def on_press(key):
    global last_key
    try:
        
        last_key = key.char
    except AttributeError:
        
        last_key = str(key).replace("Key.", "")

def start_keyboard_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


listener_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
listener_thread.start()

@app.route('/')
def home():
   
    return render_template('index.html', key_name=last_key)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
