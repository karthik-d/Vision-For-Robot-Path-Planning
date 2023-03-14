**Proof by contrdiction:**

In order to write a formal proof explaining why slice-by-slice segmentation works, we need to make some assumptions and establish some definitions first.

Assumptions:
1. The CT scan is of a single anatomical structure, such as a lung, liver, or kidney.
2. The structure is contiguous, meaning that there are no gaps or holes in the 3D volume.
3. The structure has a consistent appearance across all slices, meaning that it looks the same in each 2D image.

Definitions:

1. A voxel is a 3D pixel in the CT image, with a certain intensity value.
2. A segmentation is a labeling of voxels as belonging to either the structure of interest or the background.
Now, we can state the main theorem:

Theorem: Slice-by-slice segmentation of a contiguous anatomical structure in a 3D CT scan works, meaning that it produces a valid segmentation of the entire structure, given the assumptions above.

Proof:
We will prove this theorem by contradiction. Suppose that slice-by-slice segmentation does not work, i.e., that it produces an invalid segmentation of the entire structure. Then, there must be at least one voxel in the structure that is mislabeled by the segmentation. Let v be such a voxel.

Consider the slice that contains v. Since the structure is contiguous, there must be some neighboring voxels in the same slice that are also part of the structure. Let w be one of these voxels.

Now, we have two cases:

Case 1: The voxel v is mislabeled as background, but it should be part of the structure. In this case, the intensity value of v must be similar to the intensity value of w, since they are both part of the same structure. Therefore, if we were to use a global thresholding method to segment the entire 3D volume at once, both v and w would be labeled as part of the structure. However, since we are doing slice-by-slice segmentation, v is mislabeled because the threshold used on that particular slice was not appropriate. Therefore, this case contradicts our assumption that the structure has a consistent appearance across all slices.

Case 2: The voxel v is mislabeled as part of the structure, but it should be background. In this case, the intensity value of v must be different from the intensity value of w, since w is part of the structure and v is not. Therefore, if we were to use a global thresholding method to segment the entire 3D volume at once, v would be correctly labeled as background. However, since we are doing slice-by-slice segmentation, v is mislabeled because the threshold used on that particular slice was not appropriate. Therefore, this case contradicts our assumption that the structure is contiguous.

Since both cases lead to a contradiction, we have shown that slice-by-slice segmentation of a contiguous anatomical structure in a 3D CT scan works, given the assumptions above.