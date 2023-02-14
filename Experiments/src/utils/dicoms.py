import numpy as np 
import pandas as pd 
import pydicom as dicom
import os
from scipy import ndimage
import matplotlib.pyplot as plt

# Append and extend path as long as there is only
# one file in the directory!
def append_linear_levels(path):
	contents = os.listdir(path)
	while(len(contents)==1):
		path = os.path.join(path, contents[0])
		contents = os.listdir(path)
	return path


# Load the scans for a particular case (all slices)
# (0020, 0013) --> Tag((0x20, 0x13)) that stores the instance number (for PleThora)
def load_scan(path):
	slices = [dicom.read_file(os.path.join(path, s)) for s in os.listdir(path)]
	slices.sort(key = lambda slice: int(slice.get(dicom.tag.Tag((0x20, 0x13))).value))
	try:
		slice_thickness = np.abs(slices[0].ImagePositioncase[2] - slices[1].ImagePositioncase[2])
	except:
		slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
	# Return all slices
	for s in slices:
		s.SliceThickness = slice_thickness      
	return slices


# Get HU pixels from slices
def get_pixels_hu(slices):
	image = np.stack([s.pixel_array for s in slices])
	# Convert to int16 (from sometimes int16) 
	# should be possible as values should always be low enough (<32k)
	image = image.astype(np.int16)
	# Set outside-of-scan pixels to 0
	# The intercept is usually -1024, so air is approximately 0
	image[image == -2000] = 0    
	# Convert to Hounsfield units (HU)
	for slice_number in range(len(slices)):        
		intercept = slices[slice_number].RescaleIntercept
		slope = slices[slice_number].RescaleSlope        
		if slope != 1:
			image[slice_number] = slope * image[slice_number].astype(np.float64)
			image[slice_number] = image[slice_number].astype(np.int16)            
		image[slice_number] += np.int16(intercept)  
	# output dimension order is (DWH)  
	return np.array(image, dtype=np.int16)


# Show histogram of HU distribution
def plot_HU_distribution(case):
	case_pixels = get_pixels_hu(case)
	plt.hist(case_pixels.flatten(), bins=80, color='c')
	plt.xlabel("Hounsfield Units (HU)")
	plt.ylabel("Frequency")
	plt.show()


def plot_slice(case, slice_idx):
	plt.imshow(case[slice_idx], cmap=plt.cm.gray)
	plt.show()


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

# Order the dimensions of a nifti input into reqd form
# Specify indices of width, height and depth as 0, 1, 2
def order_dimensions(slices, op_dimensions):
	reqd_order = tuple([op_dimensions.find(x) for x in "WHD"])
	default_order = np.array([0, 1, 2])      # i.e [w,h,d]
	order = np.array([None, None, None])
	order[(reqd_order,)] = default_order
	slices = np.transpose(slices, order)
	return slices


# Check first case
"""
first_case = load_scan(append_linear_levels(os.path.join(DATA_PATH, cases[0])))
plot_HU_distribution(first_case)
plot_slice(first_case, 80)
"""

# Shape of image
"""
first_case = load_scan(append_linear_levels(os.path.join(DATA_PATH, cases[0])))
case = resample_volume(get_pixels_hu(first_case), 32, 128, 128)
case = order_dimensions(case, "DWH")
print(case.shape)
"""





