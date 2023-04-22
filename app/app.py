from flask import Flask, render_template, request, redirect, url_for
import matlab.engine
from skimage import io, transform
# import pandas as pd
import json
import plotly
import plotly.express as px
import os

from figures import preparator, sequencer
from config import *

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
        return redirect(url_for('pathplanning'))
    
    else:
        # TODO - add model
        print("ads")
        volume_container = sequencer.VolumeSliceSequencer(
            volume_path = os.path.join('assets', 'scan_6'), 
            mask_path = os.path.join('assets', 'pred_6'), 
            # gt_path = os.path.join('assets', 'gt_6'), 
            target_slice_size = (SLICE_WIDTH, SLICE_HEIGHT)
        )
        print("ads")
        volume_container.iter_with_mask()
        # volume_container.iter_with_gt()
        print("ads")
        fig = preparator.get_volume_figure(volume_container)
        print("ads")
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        print("ads")

        return render_template('set-params-path-planning.html', graphJSON=graphJSON)


@app.route('/pathplanning', methods=['GET', 'POST'])
def pathplanning():

    if request.method == 'POST':
        # Load the engine and run the path-planning files
        eng = matlab.engine.start_matlab()
        eng.run("startup_rvc.m", nargout=0)            
        eng.run("C:/Users/aniru/Vision-For-Robot-Path-Planning/path-planning/matlab-code/Pose_Schedule_with_Reschedule.m", nargout=0)    
        
        # Wait for user input before closing the figures
        input('Press Enter to Continue: ')

        return render_template('path-planning.html', loading = False)

    else:
        # Loading page
        return render_template('path-planning.html', loading = True)


if __name__ == "__main__":
    app.secret_key="secret123"
    app.run(debug=True)
