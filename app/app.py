from flask import Flask, render_template, request, redirect, url_for
#import matlab.engine

app = Flask(__name__)

@app.route('/',  methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        image_file = request.files['ct-image-file']
        try:
            image_data = image_file.read()
            print('LOG: Image data loaded!')
        except:
            print('LOG: Unable to load image.')

        # TODO - load the model, run inference and save the output

        return redirect(url_for('predict'))

    else:
        return render_template('model-prediction.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        pass
    
    else:
        # TODO - pass actual img filename
        return render_template('set-params-path-planning.html', image = 'segmented-output-sample.png')


if __name__ == "__main__":
    app.secret_key="secret123"
    app.run(debug=True)
