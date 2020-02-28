import numpy as np
from scipy.ndimage import binary_erosion,binary_dilation,affine_transform
from LucasKanadeAffine import*
import cv2

def SubtractDominantMotion(image1, image2):
	# Input:
	#	Images at time t and t+1 
	# Output:
	#	mask: [nxm]
    # put your implementation here
    
    threshold = 0.7
    rows,cols= np.shape(image1)
    mask = np.ones(image1.shape, dtype=bool)
    
    M = LucasKanadeAffine(image1, image2)
    It_warp = cv2.warpAffine(image1,M,(cols,rows))
    It_warp = binary_dilation(It_warp)
    It_warp = binary_erosion(It_warp)
    difference = np.abs(image2 - It_warp)
    location = np.where(difference > threshold)
    mask = np.array(location).T
    
    
    return mask
