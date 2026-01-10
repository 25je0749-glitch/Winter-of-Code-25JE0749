import threading
from flask import Flask, render_template
from pynput import keyboard

app = Flask(__name__)

key_count = 0

def on_press(key):
    global key_count
    
    key_count += 1

def start_keyboard_listener():
    
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


listener_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
listener_thread.start()

@app.route('/')
def home():
   
    return render_template('index.html', count=key_count)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
