import numpy as np
import keras
import glob

from .path_manager import append_linear_levels
from utils import niftis, dicoms, niftis
from config import *


class InputSequencer(keras.utils.Sequence):
	"""
	Base sequencer class for all datasets
	"""

	def __init__(self, shuffle=True):		
		self.shuffle = shuffle		
		self.BATCH_SIZE = BATCH_SIZE
		self.IMG_SIZE = IMG_SIZE    # As (width, height, channels)

	def get_instance_paths(self, root_path, dataformat='nifti'):

		if dataformat == 'nifti':
			instance_paths = sorted(glob.glob(os.path.join(root_path, "*.nii")))
			full_paths = []
			
			for scan in instance_paths:
				path_ = os.path.join(root_path, scan)
				full_paths.append(append_linear_levels(path_, True))
			return full_paths

		elif dataformat == 'dicom':
			instance_paths = sorted(glob.glob(os.path.join(root_path, "*.dcm")))
			full_paths = []
			
			for scan in instance_paths:
				path_ = os.path.join(root_path, scan)
				full_paths.append(append_linear_levels(path_, False))
			return full_paths

		else:
			return None

	def on_epoch_end(self):
		if(self.shuffle):
			np.random.shuffle(self.indexes)

	def __len__(self):
		return len(self.scan_paths) // self.BATCH_SIZE

	def __getitem__(self, idx):
		"""Returns tuple (input, target) correspond to batch #idx."""
		i = (idx+self.idx_adjust) * self.BATCH_SIZE
		indices = self.indexes[i : i + self.BATCH_SIZE]
		
		batch_scan_paths = [ self.scan_paths[idx] 
								for idx in indices ]
		batch_annot_paths = [ self.annot_paths[idx] 
								for idx in indices ]

		x = []
		y = []

		for scan_path, annot_path in zip(batch_scan_paths, batch_annot_paths):
			try:
				# Load Scans (x-data)
				if self.scan_format == 'dicom':
					scan = dicoms.load_scan(scan_path)
					scan = dicoms.get_pixels_hu(scan)
					#scan = dicoms.order_dimensions(scan, "DWH")
					scan = dicoms.resample_volume(scan, *(self.IMG_SIZE[:3]), 'CUBIC')
					scan = np.expand_dims(scan, axis=-1)
				elif self.scan_format == 'nifti':
					scan = niftis.load_scan(scan_path)
					# Requires reordering
					#scan = niftis.order_dimensions(scan, "DWH")
					#scan = niftis.resample_volume(scan, *(self.IMG_SIZE[:3]), 'CUBIC')
					scan = np.expand_dims(scan, axis=-1)
				# Load Annotations (y-data)
				if self.annot_format == 'dicom':
					annot = dicoms.load_scan(annot_path)
					annot = dicoms.get_pixels_hu(annot)
					#annot = dicoms.order_dimensions(annot, "DWH")
					annot = dicoms.resample_volume(annot, *(self.IMG_SIZE[:3]), 'NEAREST_N')
					annot = np.expand_dims(annot, axis=-1)
				elif self.annot_format == 'nifti':
					annot = niftis.load_scan(annot_path)
					# Requires reordering
					#annot = niftis.order_dimensions(annot, "DWH")
					#annot = niftis.resample_volume(annot, *(self.IMG_SIZE[:3]), 'NEAREST_N')
					annot = np.expand_dims(annot, axis=-1)
			
			except Exception as e:
				print(e)
				subst_idx = np.random.randint(0, len(self.scan_paths))
				batch_scan_paths.append(self.scan_paths[subst_idx])
				batch_annot_paths.append(self.annot_paths[subst_idx])

			else:
				x.append(scan)
				y.append(annot)

		return np.array(x), np.array(y)

	
def test_run():
	
	skips = []
	scan_paths = sorted(os.listdir(PLETHORA_SCAN_PATH))
	scans = []
	ctr = 0
	for scan in scan_paths:
		ctr += 1
		try:
			path_ = os.path.join(PLETHORA_SCAN_PATH, scan)
			scan = append_linear_levels(path_, False)
			scan = dicoms.load_scan(scan)
			scan = dicoms.get_pixels_hu(scan)
			scan = dicoms.resample_volume(scan, 32, 128, 128)
			scan = dicoms.order_dimensions(scan, "DWH")
		except Exception as e:
			#print(e)
			skips.append(ctr)
		else:
			scan = np.expand_dims(scan, axis=-1)
			scans.append(scan)
		if ctr>5:
			break
	print("{count} Scans Loaded".format(count=len(scans)))
	scans = np.array(scans)
	
	print("Loading Annotations")
	annotation_paths = sorted(os.listdir(PLETHORA_LUNGMASK_PATH))
	annotations = []
	ctr = 0
	for annot in annotation_paths:
		ctr += 1
		try:
			path_ = os.path.join(PLETHORA_LUNGMASK_PATH, annot)
			annot = append_linear_levels(path_, True)
			annot = niftis.load_scan(annot)
			annot = niftis.resample_volume(annot, 32, 128, 128)
			annot = niftis.order_dimensions(annot, "DWH")
		except Exception as e:
			print(e)
		else:
			if ctr not in skips:
				annot = np.expand_dims(annot, axis=-1)
				annotations.append(annot)
		if ctr>5:
			break
	print("{count} Annotations Loaded".format(count=len(annotations)))
	annotations = np.array(annotations)

	# Load model
	model = get_model()
	model.summary()
	# Set params
	initial_learning_rate = 0.0001
	# Add LR schedule
	metrics = ["acc"]
	model.compile(
		loss="binary_crossentropy",
		optimizer=keras.optimizers.Adam(),
		metrics=metrics,
	)