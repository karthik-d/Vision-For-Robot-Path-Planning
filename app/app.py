from flask import Flask, render_template
#import matlab.engine

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('model-prediction.html')

if __name__ == "__main__":
    app.secret_key="secret123"
    app.run(debug=True)
