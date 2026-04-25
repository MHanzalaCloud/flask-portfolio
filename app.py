from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f'<h1>Hello from Flask!</h1><p>Server time: {current_time}</p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
