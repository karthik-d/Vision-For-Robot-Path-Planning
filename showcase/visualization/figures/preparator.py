import plotly.graph_objects as go
import numpy as np

from config import *


def get_slice_figure(slice_array, num_frames=68):

	width, height = slice_array.shape

	fig = go.Figure(
		frames = [go.Frame(
			data = go.Surface(
				z = (6.7 - k * 0.1) * np.ones((width, height)),
				surfacecolor = np.flipud(slice_array),
		    	cmin = 0, 
				cmax = 200
		),
		name=str(k))
		for k in range(num_frames)]
	)

	# data payload
	fig.add_trace(go.Surface(
		z = (6.7 * np.ones((width, height))),
		surfacecolor = np.flipud(slice_array),
		colorscale='Gray',
		cmin = 0, 
		cmax = 200,
		colorbar = dict(thickness=20, ticklen=4)
		)
	)

	# configure layout
	fig.update_layout(
		title = 'Slices in volumetric data',
        width = FIG_WIDTH,
        height = FIG_HEIGHT,
    	scene = pack_scene_config(),
    	updatemenus = [ pack_update_menu_config() ],
        sliders = pack_slider_config(fig)
)

