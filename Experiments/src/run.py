from data.isles18 import Isles18Sequencer
import matplotlib.pyplot as plot 

from config import *


test_sequencer = Isles18Sequencer(ISLES18_TEST_PATH, 'nifti', ISLES18_TEST_PATH, 'nifti')
img, annot = test_sequencer[0]

print(img.shape)
print(annot.shape)

plot.imshow(img[0, :, :, 0, 0])
plot.show()

print("ran!")