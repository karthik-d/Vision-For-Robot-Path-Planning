import numpy as np
import nibabel as nib 
from scipy import ndimage
import os


# Append and extend path as long as there is only
# one file in the directory!
def append_linear_levels(path):
	contents = os.listdir(path)
	while(len(contents)==1):
		path = os.path.join(path, contents[0])
		if os.path.isdir(contents[0]):
			contents = os.listdir(path)
		else:
			break
	return path


# Order the dimensions of a nifti input into reqd form
# Specify indices of width, height and depth as 0, 1, 2
def order_dimensions(slices, op_dimensions, from_=None):
	reqd_order = tuple([op_dimensions.find(x) for x in "WHD"])
	if from_ is None:
		default_order = np.array([1, 0, 2])      # i.e [h,w,d]
	else:
		default_order = np.array([from_.find(x) for x in "WHD"])
	order = np.array([None, None, None])
	order[(reqd_order,)] = default_order
	slices = np.transpose(slices, order)
	return slices


def load_scan(path, invert_RL=False, invert_AP=False, invert_SI=False):
	data = nib.load(path)
	# Make inversions as necessary
	data = invert_dimensions(data, invert_RL, invert_AP, invert_SI)
	# Extract pixels and np array
	slices = data.get_fdata()
	# output dimension order is (HWD)  
	return slices


def invert_dimensions(data, invert_RL=False, invert_AP=False, invert_SI=False):
	# Make inversions as necessary
	ornt = [
		[0, 1],
		[1, 1],
		[2, 1]
	]
	# Change reqd orientations
	if invert_RL:
		ornt[0][1] = -1		
	if invert_AP:
		ornt[1][1] = -1
	if invert_SI:
		ornt[2][1] = -1
	data = data.as_reoriented(ornt)
	# Return reoriented data
	return data


def resample_volume(case, reqd_slices, reqd_width, reqd_height, interpolate_method='CUBIC'):
	# Input image must be ordered as (DWH)
	curr_slices = case.shape[0]
	curr_width = case.shape[1]
	curr_height = case.shape[2]
	# Compute change factor
	depth_factor = reqd_slices/curr_slices
	width_factor = reqd_width/curr_width
	height_factor = reqd_height/curr_height
	# Resize across z-axis
	case = ndimage.zoom(case, (depth_factor, width_factor, height_factor), order=SPLINE_ORDER[interpolate_method])
	return case