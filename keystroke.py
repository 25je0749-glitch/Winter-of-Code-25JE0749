import threading
from flask import Flask, render_template
from pynput import keyboard

app = Flask(__name__)

# Global variable to store the key count
key_count = 0

def on_press(key):
    global key_count
    # Every time a key is pressed, increase the count by 1
    key_count += 1

def start_keyboard_listener():
    # This starts the keyboard listener in the background
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Start the listener in a separate thread immediately
listener_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
listener_thread.start()

@app.route('/')
def home():
    # Only send the key count to the website
    return render_template('index.html', count=key_count)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
