import psutil
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # 1. Get CPU usage (percentage)
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # 2. Get Memory usage (percentage)
    memory_percent = psutil.virtual_memory().percent
    
    # 3. Send these numbers to the HTML file
    return render_template('index.html', cpu=cpu_percent, ram=memory_percent)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
