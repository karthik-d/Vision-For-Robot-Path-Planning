from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px


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
    


if __name__ == '__main__':
    app.run(debug=True)