from flask import Flask, render_template, request
#import matlab.engine

app = Flask(__name__)


@app.route('/',  methods=["GET", "POST"])
def predict():
    if request.method == 'POST':
        image_file = request.files['ct-image-file']
        try:
            image_data = image_file.read()
            print('LOG: Image data loaded!')
        except:
            print('LOG: Unable to load image.')

        # TODO - load the model and run inference

        return render_template('path-planning.html')

    else:
        return render_template('model-prediction.html')

if __name__ == "__main__":
    app.secret_key="secret123"
    app.run(debug=True)
