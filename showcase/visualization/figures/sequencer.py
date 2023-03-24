from skimage import io
import numpy as np
import os


class VolumeSliceSequencer:

    def __init__(self, volume_path, target_slice_size=None, batching_size=None):
        
        self.batching_size = batching_size
        self.target_slice_size = target_slice_size
        # assume all images in the path are slices in a sorted order
        if not os.path.exists(volume_path):
            self.volume = io.imread("https://s3.amazonaws.com/assets.datacamp.com/blog_assets/attention-mri.tif")
            return None

        volume = []
        for slice_f in sorted(os.listdir(volume_path)):
            slice_ = io.imread(os.path.join(volume_path, slice_f))
            if target_slice_size is not None:
                transform.resize(slice_, self.target_slice_size)
            volume.append(slice_)
        self.volume = np.array(volume)

    def __iter__(self):
        
        if self.batching_size is None:
            yield self.volume 

        else:
            for i in range(0, self.volume.shape[0], self.batching_size):
                yield self.volume[i:i+self.batching_size]


tester = VolumeSliceSequencer(os.path.join('..', 'assets', 'scan_6'))
for i in tester:
    print(i.shape)