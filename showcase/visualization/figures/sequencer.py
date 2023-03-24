from skimage import io, transform
import numpy as np
import os

from matplotlib import pyplot as plot


class VolumeSliceSequencer:

    def __init__(self, volume_path, mask_path=None, target_slice_size=None, batching_size=None):
            
        self.volume_path = volume_path
        self.mask_path = mask_path
        self.batching_size = batching_size
        self.target_slice_size = target_slice_size

        # assume all images in the path are slices in a sorted order
        if not os.path.exists(self.volume_path):
            self.volume = io.imread("https://s3.amazonaws.com/assets.datacamp.com/blog_assets/attention-mri.tif")
        else:
            self.volume = self._load_volume()
            print(self.volume.shape)
            
        if self.mask_path is None or not os.path.exists(self.mask_path):
            self.mask = np.zeros(self.volume.shape) 
        else:
            self.mask = self._load_mask()
        
        # by default, loads without mask when iterating
        self.iter_without_mask()

        # patching to support basic 'array queries'
        # TODO: Make subclass of ndarray
        # drop the channel dimension
        self.shape = (self.volume.shape[:3]) if self.batching_size is None else (self.batching_size, *self.volume.shape[1:3])

        # normalization for colorscale -- reserve 1.0 for mask
        self.volume /= 255
        self.volume[self.mask==1.0] = 0.99

    def iter_with_mask(self):
        self.apply_mask = False

    def iter_without_mask(self):
        self.apply_mask = True
    
    def _load_volume(self):
        volume = []
        for slice_f in sorted(os.listdir(self.volume_path)):
            slice_ = io.imread(os.path.join(self.volume_path, slice_f))
            if self.target_slice_size is not None:
                slice_ = transform.resize(slice_, self.target_slice_size, order=0)
                # make three-channel
                slice_ = np.transpose(np.tile(slice_, (3, 1, 1)), (1, 2, 0))
                print(slice_.min(), slice_.max())
            volume.append(slice_)
        return np.array(volume)

    def _load_mask(self):
        mask = []
        for slice_f in sorted(os.listdir(self.mask_path)):
            slice_ = io.imread(os.path.join(self.mask_path, slice_f))
            if self.target_slice_size is not None:
                slice_ = transform.resize(slice_, self.target_slice_size, order=0)
            mask.append(slice_)
        return np.array(mask)

    def __getitem__(self, idx):
        return self.volume[idx]
    
    def __iter__(self):
        
        if self.batching_size is None:
            for slice_ in self.volume:
                yield slice_ 
        else:
            for i in range(0, self.volume.shape[0], self.batching_size):
                yield self.volume[i:i+self.batching_size]


# tester = VolumeSliceSequencer(os.path.join('..', 'assets', 'scan_6'), target_slice_size=(50, 50))
# for i in tester:
#     print(i.shape)