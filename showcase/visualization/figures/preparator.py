import plotly.graph_objects as go
import numpy as np

from config import *


def get_slice_figure(slice_array):

	width, height = slice_array.shape

	fig = go.Figure(
		frames = [go.Frame(
			data = go.Surface(
				z = (6.7 - k * 0.1) * np.ones((width, height)),
				surfacecolor = np.flipud(volume[67 - k]),
		    	cmin = 0, 
				cmax = 200
		),
		name=str(k))
		for k in range(nb_frames)]
	)

	# data payload
	fig.add_trace(go.Surface(
		z = (6.7 * np.ones((width, height))),
		surfacecolor = np.flipud(volume[67]),
		colorscale='Gray',
		cmin = 0, 
		cmax = 200,
		colorbar = dict(thickness=20, ticklen=4)
		)
	)
