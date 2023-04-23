from flask import Flask, render_template, request, redirect, url_for
import matlab.engine
from skimage import io, transform
# import pandas as pd
import numpy as np
import json
import plotly
import plotly.express as px
import os

from figures import preparator, sequencer
from config import *


TARGET = []
OBSTACLE = []

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
        return render_template('result-visualization.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the values for target and obstacle from the form
        target = [request.form.get(f'target{i}') for i in range(1, 4)]
        obstacle = [request.form.get(f'obstacle{i}') for i in range(1, 4)]
        
        # Convert the values to integers
        target = [int(x) for x in target]
        obstacle = [int(x) for x in obstacle if x != '']
        
        # Print the values for testing
        print("Target:", target)
        print("Obstacle:", obstacle)

        global TARGET, OBSTACLE
        TARGET = target
        OBSTACLE = obstacle
         
        return redirect(url_for('pathplanning'))
    
    else:
        # TODO - add model
        volume_container = sequencer.VolumeSliceSequencer(
            volume_path = os.path.join('assets', 'scan_6'), 
            mask_path = os.path.join('assets', 'pred_6'), 
            # gt_path = os.path.join('assets', 'gt_6'), 
            target_slice_size = (SLICE_WIDTH, SLICE_HEIGHT)
        )
        volume_container.iter_with_mask()
        # volume_container.iter_with_gt()
        fig = preparator.get_volume_figure(volume_container)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('set-params-path-planning.html', graphJSON=graphJSON)


@app.route('/pathplanning', methods=['GET', 'POST'])
def pathplanning():

    if request.method == 'POST':
        global TARGET

        # Load the engine and run the path-planning files
        eng = matlab.engine.start_matlab()
        eng.addpath('C:/Users/aniru/Vision-For-Robot-Path-Planning/path-planning/matlab-code')

        eng.startup_rvc(nargout=0)            
        eng.Pose_Schedule_with_Reschedule(matlab.double(TARGET), nargout=0)

        # Get a list of all running MATLAB engines
        matlab_engines = matlab.engine.find_matlab()

        # Keep the engine running until the user explicitly closes it
        while len(matlab_engines) > 0:
            matlab_engines = matlab.engine.find_matlab()    
        
        # Wait for user input before closing the figures
        #input('Press Enter to Continue: ')

        #return render_template('path-planning.html', loading = False)

    else:
        # Loading page
        return render_template('path-planning.html', loading = True)

@app.route('/complete')
def complete():
    return render_template('complete.html')

if __name__ == "__main__":
    app.secret_key="secret123"
    app.run(debug=True)
