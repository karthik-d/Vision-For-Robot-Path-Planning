from matplotlib import pyplot as plot


def pack_frame_config(duration):
   
    return {
		"frame": {"duration": duration},
		"mode": "immediate",
		"fromcurrent": True,
		"transition": {"duration": duration, "easing": "linear"},
	}


def pack_slider_config(figure, duration=0):

	return [
		{
			"pad": {"b": 10, "t": 60},
			"len": 0.9,
			"x": 0.1,
			"y": 0,
			"steps": [
				{
					"args": [[f.name], pack_frame_config(duration)],
					"label": str(k),
					"method": "animate",
				}
				for k, f in enumerate(figure.frames)
			],
		}
	]


def pack_update_menu_config(play_bt_dur=50, pause_bt_dur=0):

	return {
		"buttons": [
			{
				"args": [None, pack_frame_config(play_bt_dur)],
				"label": "&#9654;", # play symbol
				"method": "animate",
			},
			{
				"args": [[None], pack_frame_config(pause_bt_dur)],
				"label": "&#9724;", # pause symbol
				"method": "animate",
			},
		],
		"direction": "left",
		"pad": {"r": 10, "t": 70},
		"type": "buttons",
		"x": 0.1,
		"y": 0,
	}


def pack_scene_config(num_frames):
	
	return {
		'zaxis': {'range': [-0.1, num_frames/10 + 1], 'autorange': False},
		'aspectratio': {'x': 1, 'y': 1, 'z': 1}
	}


FIG_WIDTH = 600
FIG_HEIGHT = 600

SLICE_WIDTH = 50
SLICE_HEIGHT = 50


# gray_cmap = plt.get_cmap("gray")
# Standard Scaling: 0-255 to 0.1-0.9
PLOT_COLORSCALE = [[0.0, 'rgb(0, 0, 200)']] # for second mask
PLOT_COLORSCALE.extend([
	[(0.1+(x*0.8)/255), f'rgb({x},{x},{x})']
	for x in range(255)
])
PLOT_COLORSCALE.append([1.0, 'rgb(100, 0, 0)']) # for masks

PLOT_OPACITYSCALE = [
	[x/256, 1]
	for x in range(255)
]
PLOT_OPACITYSCALE.append([1.0, 0.4])
PLOT_OPACITYSCALE.append([0.0, 0.4])