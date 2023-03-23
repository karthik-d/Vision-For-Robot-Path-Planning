from flask import Flask
import matlab.engine

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == "__main__":
    app.secret_key="secret123"
    app.run(debug=True)