import numpy as np
import scipy
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.patches as patches
from LucasKanade import *

# write your script here, we recommend the above libraries for making your animation



    
frames = np.load('../data/carseq.npy')
num_frames = np.shape(frames)[2]
rects = np.zeros((num_frames,4))
x1,y1,x2,y2 = 59,116,145,151
for i in range(num_frames-1):
    
    It = frames[:,:,i]
    It1 = frames[:,:,i+1]
    rect = np.array([x1,y1,x2,y2]).T
    rects[i,:] = rect.T
    
   
    if i % 100 == 0:
        plt.figure()
        ax1 = plt.gca()
        ax1.add_patch(patches.Rectangle([x1,y1],width=x2-x1,height=y2-y1,fill=None,color='r'))
        plt.imshow(It1,cmap='gray')
    plt.show()
    
    p = LucasKanade(It, It1, rect, p0 = np.zeros(2))
    x1,y1,x2,y2 = np.floor(x1+p[0]),np.floor(y1+p[1]),np.floor(x2+p[0]),np.floor(y2+p[1])
    rect  = np.array([x1,y1,x2,y2]).T
    rects[i+1,:] = rect.T
    print(rect.T)
        
np.save('carseqrects.npy',rects)