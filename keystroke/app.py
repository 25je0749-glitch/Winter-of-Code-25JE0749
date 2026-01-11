from flask import Flask, render_template
from pynput import keyboard

app = Flask(__name__)

key_count = 0

def on_press(key):
    global key_count
    key_count += 1

listener = keyboard.Listener(on_press=on_press)
listener.start()

@app.route('/')
def home():
    return render_template('index.html')

# --- THIS IS THE MISSING PART ---
@app.route('/update_count')
def update_count():
    return str(key_count)
# --------------------------------

if __name__ == "__main__":
    app.run(debug=True)
