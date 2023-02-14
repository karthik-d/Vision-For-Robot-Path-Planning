from ..utils import niftis, InputSequencer


class Isles18Sequencer(InputSequencer.InputSequencer):

    def __init__(self, scan_dir_path, scan_format, annot_dir_path, annot_format, shuffle=True):
        
        super().__init__(shuffle)
		# Get all scans and image paths
        self.scan_paths = self.get_instance_paths(scan_dir_path, scan_format)
		self.scan_format = scan_format
		self.annot_paths = self.get_instance_paths(annot_dir_path, annot_format)
		self.annot_format = annot_format
		self.indexes = np.arange(len(self.scan_paths))
		self.idx_adjust = 0
		self.on_epoch_end()