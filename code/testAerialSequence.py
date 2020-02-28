import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.patches as patches
from SubtractDominantMotion import *

# write your script here, we recommend the above libraries for making your animation
frames_aerial = np.load('../data/aerialseq.npy')
num_frames = np.shape(frames_aerial)[2]
masks = []
for i in range(num_frames-1):
    image1 = frames_aerial[:,:,i]
    image2 = frames_aerial[:,:,i+1]
    mask = SubtractDominantMotion(image1, image2)
    masks.append([mask])
    print(np.shape(mask))
    if i % 30 == 0:
        plt.figure()
        ax1 = plt.gca()
        plt.imshow(image1,cmap='gray')
        plt.scatter(mask[:,1],mask[:,0],alpha=0.5,c='royalblue',s=0.5)
        
    plt.show()

np.save('aerialseqrects.npy',rects)