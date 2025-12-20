import threading
from flask import Flask, render_template
from pynput import keyboard

app = Flask(__name__)

# Global variable to store the LAST key pressed
last_key = "Waiting..."

def on_press(key):
    global last_key
    try:
        # Try to get the normal letter (a, b, c, 1, 2)
        last_key = key.char
    except AttributeError:
        # If it's a special key (Space, Enter, Shift), convert it to a string
        last_key = str(key).replace("Key.", "")

def start_keyboard_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Start the listener in the background
listener_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
listener_thread.start()

@app.route('/')
def home():
    # Send the last_key variable to the website
    return render_template('index.html', key_name=last_key)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
