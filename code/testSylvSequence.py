import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.patches as patches

# write your script here, we recommend the above libraries for making your animation
bases = np.load('../data/sylvbases.npy')
frames = np.load('../data/sylvseq.npy')
#bases_reshape = bases.reshape(47*55,10)
#bases_reshape_0 = bases_reshape[:,1] @ bases_reshape[:,1].T

num_frames = np.shape(frames)[2]
rects = np.zeros((num_frames,4))# rects container for LK basis
rects_original = np.zeros((num_frames,4))#rects container for Lk
x1,y1,x2,y2 = 101,61,156,108
rects[0,:] = np.array([x1,y1,x2,y2])
rects_original[0,:] = np.array([x1,y1,x2,y2])

for i in range(num_frames-1):
    
    It = frames[:,:,i]
    It1 = frames[:,:,i+1]

    rect = rects[i,:] 
    rect_original = rects_original[i,:]
    [x1,y1,x2,y2] = rect
    [x1_original,y1_original,x2_original,y2_original] = rect_original
   
    if i % 50 == 0:
        plt.figure()
        ax1 = plt.gca()
        ax1.add_patch(patches.Rectangle([x1,y1],width=x2-x1,height=y2-y1,fill=None,color='g'))
        ax1.add_patch(patches.Rectangle([x1_original,y1_original],width=x2_original-x1_original,height=y2_original-y1_original,fill=None,color='r'))
        plt.imshow(It1,cmap='gray')
        
    plt.show()
    
    p = LucasKanadeBasis(It, It1, rect, bases)
    p_original = LucasKanade(It, It1, rect_original, p0 = np.zeros(2))
    x1,y1,x2,y2 = np.floor(x1+p[0]),np.floor(y1+p[1]),np.floor(x2+p[0]),np.floor(y2+p[1])
    x1_original,y1_original,x2_original,y2_original = np.floor(x1_original+p_original[0]),np.floor(y1_original+p_original[1]),np.floor(x2_original+p_original[0]),np.floor(y2_original+p_original[1])
    rect  = np.array([x1,y1,x2,y2])
    rect_original = np.array([x1_original,y1_original,x2_original,y2_original] )
    rects[i+1,:] = rect
    rects_original[i+1,:] = rect_original
    print(rect.T)

np.save('sylvseqrects.npy',rects)
#for i in range(10):
#   plt.figure()
#   plt.imshow(bases[:,:,i],cmap='gray')
#
#plt.show()

