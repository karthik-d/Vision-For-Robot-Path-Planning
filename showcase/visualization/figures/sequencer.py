from skimage import io, transform
import numpy as np
import os

from matplotlib import pyplot as plot


class VolumeSliceSequencer:

    def __init__(self, volume_path, mask_path=None, gt_path=None, target_slice_size=None, batching_size=None):
            
        self.volume_path = volume_path
        self.mask_path = mask_path
        self.gt_path = gt_path
        self.batching_size = batching_size
        self.target_slice_size = target_slice_size

        # assume all images in the path are slices in a sorted order
        if not os.path.exists(self.volume_path):
            self.volume = io.imread("https://s3.amazonaws.com/assets.datacamp.com/blog_assets/attention-mri.tif")
        else:
            self.volume = self._load_volume()
            
        if self.mask_path is None or not os.path.exists(self.mask_path):
            self.mask = np.zeros(self.volume.shape) 
        else:
            self.mask = self._load_mask()

        if self.gt_path is None or not os.path.exists(self.gt_path):
            self.gt = np.zeros(self.volume.shape) 
        else:
            self.gt = self._load_gt()
        
        # by default, loads without mask when iterating
        self.iter_without_mask()
        self.iter_without_gt()

        # patching to support basic 'array queries'
        # TODO: Make subclass of ndarray
        # drop the channel dimension
        self.shape = (self.volume.shape[:3]) if self.batching_size is None else (self.batching_size, *self.volume.shape[1:3])

        # normalization for colorscale -- reserve 1.0 for mask
        self.volume[self.volume>250] = 250
        # self.volume[self.volume<30] = 30

    def iter_with_mask(self):
        self.apply_mask = True

    def iter_without_mask(self):
        self.apply_mask = False

    def iter_with_gt(self):
        self.apply_gt = True

    def iter_without_gt(self):
        self.apply_gt = False
    
    def _load_volume(self):
        volume = []
        for slice_f in sorted(os.listdir(self.volume_path)):
            slice_ = io.imread(os.path.join(self.volume_path, slice_f))
            if self.target_slice_size is not None:
                slice_ = transform.resize(slice_, self.target_slice_size, order=0)
                # # make three-channel
                # slice_ = np.transpose(np.tile(slice_, (3, 1, 1)), (1, 2, 0))
            volume.append(slice_)
        return np.array(volume)

    def _load_mask(self):
        mask = []
        for slice_f in sorted(os.listdir(self.mask_path)):
            slice_ = io.imread(os.path.join(self.mask_path, slice_f))
            if self.target_slice_size is not None:
                slice_ = transform.resize(slice_, self.target_slice_size, order=0)
                slice_[slice_<127] = 0
                slice_[slice_>=127] = 255
            mask.append(slice_)
        return np.array(mask)

    def _load_gt(self):
        mask = []
        for slice_f in sorted(os.listdir(self.gt_path)):
            slice_ = io.imread(os.path.join(self.gt_path, slice_f))
            if self.target_slice_size is not None:
                slice_ = transform.resize(slice_, self.target_slice_size, order=0)
                slice_[slice_<127] = 0
                slice_[slice_>=127] = 255
            mask.append(slice_)
        return np.array(mask)

    def __getitem__(self, idx):
        return self.volume[idx]
    
    def __iter__(self):
        
        volume = self.volume.copy()
        if self.apply_mask:
            volume[self.mask>127] = 255

        # if self.apply_gt:
        #     volume[self.gt>127] = 0

        if self.batching_size is None:
            for i, slice_ in enumerate(volume):
                yield slice_ 
        else:
            for i in range(0, volume.shape[0], self.batching_size):
                yield volume[i:i+self.batching_size]


# tester = VolumeSliceSequencer(os.path.join('..', 'assets', 'scan_6'), target_slice_size=(50, 50))
# for i in tester:
#     print(i.shape)