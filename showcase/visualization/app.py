from flask import Flask, render_template
from skimage import io, transform
import pandas as pd
import json
import plotly
import plotly.express as px
import os

from figures import preparator
from config import *


app = Flask(__name__)

@app.route('/viz/test')
def test_figure():
    df = pd.DataFrame({
        'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 'Bananas'],
        'Amount': [4, 1, 2, 2, 4, 5],
        'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
    })   
    fig = px.bar(df, x='Fruit', y='Amount', color='City', barmode='group')   
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)   
    return render_template('fig-container.html', graphJSON=graphJSON)


@app.route('/viz/slice')
def slice_figure():
    fig = preparator.get_slice_figure(
        transform.resize(
            io.imread(os.path.join('assets', 'scan_6', '27_in.jpg')).T,
            (SLICE_WIDTH, SLICE_HEIGHT),
            order=0
        )
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)   
    return render_template('fig-container.html', graphJSON=graphJSON)


@app.route('/viz/volume')
def volume_figure():
    # fig = preparator.get_slice_figure(
    #     transform.resize(
    #         io.imread(os.path.join('assets', 'scan_6', '27_in.jpg')).T,
    #         (SLICE_WIDTH, SLICE_HEIGHT),
    #         order=0
    #     )
    # )
    vol = io.imread("https://s3.amazonaws.com/assets.datacamp.com/blog_assets/attention-mri.tif")
    fig = preparator.get_volume_figure(vol)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)   
    return render_template('fig-container.html', graphJSON=graphJSON)


if __name__ == '__main__':
    app.run(debug=True)