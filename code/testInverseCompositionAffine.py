# -*- coding: utf-8 -*-
import numpy as np
from scipy.ndimage import binary_erosion,binary_dilation,affine_transform
from InverseCompositionAffine import*
import cv2

def Subtract(image1, image2):
	# Input:
	#	Images at time t and t+1 
	# Output:
	#	mask: [nxm]
    # put your implementation here
    
    threshold = 0.7
    rows,cols= np.shape(image1)
    mask = np.ones(image1.shape, dtype=bool)
    
    M = InverseCompositionAffine(image1, image2)
    It_warp = cv2.warpAffine(image1,M,(cols,rows))
    It_warp = binary_dilation(It_warp)
    It_warp = binary_erosion(It_warp)
    difference = np.abs(image2 - It_warp)
    location = np.where(difference > threshold)
    mask = np.array(location).T
    
    
    return mask

frames_aerial_1 = np.load('../data/aerialseq.npy')
num_frames = np.shape(frames_aerial)[2]
masks = []
for i in range(num_frames-1):
    image1 = frames_aerial_1[:,:,i]
    image2 = frames_aerial_1[:,:,i+1]
    mask = Subtract(image1, image2)
    masks.append([mask])
    print(np.shape(mask))
    if i % 30 == 0:
        plt.figure()
        ax1 = plt.gca()
        plt.imshow(image1,cmap='gray')
        plt.scatter(mask[:,1],mask[:,0],alpha=0.5,c='royalblue',s=0.5)
        
    plt.show()
    
np.save('aerialseqrects(InverseComposition).npy',rects)