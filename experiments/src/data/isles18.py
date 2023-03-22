from utils import niftis, input_sequencer
import numpy as np
from typing_extensions import override
import glob
import os


class Isles18Sequencer(input_sequencer.InputSequencer):

	def __init__(self, scan_dir_path, scan_format, annot_dir_path, annot_format, shuffle=True):
		
		super().__init__(shuffle)
		# Get all scans and image paths
		self.scan_paths = self.get_instance_paths(scan_dir_path, scan_format)
		self.scan_format = scan_format
		print("[INFO] Found {} scans.".format(len(self.scan_paths)))
		print(self.scan_paths[-1:])

		self.annot_paths = self.get_instance_paths(annot_dir_path, annot_format)
		self.annot_format = annot_format
		print("[INFO] Found {} annotations.".format(len(self.annot_paths)))
		print(self.annot_paths[-1:])
		
		self.indexes = np.arange(len(self.scan_paths))
		self.idx_adjust = 0
		self.on_epoch_end()
	
	@override
	def get_instance_paths(self, root_path, dataformat='nifti'):

		data_ext = '.nii' if dataformat=='nifti' else 'dcm'
		full_paths = []
		for curr_path, dirnames, filenames in os.walk(root_path):
			full_paths.extend([
				os.path.join(curr_path, fi) for fi in filter(lambda x: isinstance(x, str) and x.endswith(data_ext), filenames)
			])

		return full_paths