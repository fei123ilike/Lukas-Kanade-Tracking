import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.patches as patches
from LucasKanade import *
# write your script here, we recommend the above libraries for making your animation
def LucasKanade_1_to_n(It1, Itn, p_init, rect1, rectn):
    p = np.zeros(2)
    
    x1,y1 = rect1[0],rect1[1] #top left corner of rect1
    x2,y2 = rect1[2],rect1[3] #bottom right corner of rect1
    
    threshold = 0.1
    count = 0
    max_count = 100
    delta_p_l2 = 100
    num_row = np.shape(It1)[0]
    num_col = np.shape(It1)[1]

    Grad_Itn_y,Grad_Itn_x = np.gradient(Itn)
  
    It1_spline = RectBivariateSpline(np.arange(num_row),np.arange(num_col),It1)
    Itn_spline = RectBivariateSpline(np.arange(num_row),np.arange(num_col),Itn)
    
    Grad_x_spline = RectBivariateSpline(np.arange(num_row),np.arange(num_col),Grad_Itn_x)
    Grad_y_spline = RectBivariateSpline(np.arange(num_row),np.arange(num_col),Grad_Itn_y)
    
    while delta_p_l2 > threshold and count < max_count:
        count += 1
        #warp orginal coordinate
        W = np.array([[1,0,p[0]],
                      [0,1,p[1]]]) # warp matrix
        Jacobian_W = np.array([[1,0],
                               [0,1]]) # jacobian matrix of W
        
        x1_n,y1_n = rectn[0],rectn[1] #top left corner
        x2_n,y2_n = rectn[2],rectn[3] #bottom right corner
        top_left_n = np.array([x1_n,y1_n,1]).T
        bot_right_n = np.array([x2_n,y2_n,1]).T
        top_left_warp = W @ top_left_n
        bot_right_warp = W @ bot_right_n
        warp_x1,warp_y1 = (top_left_warp[0]),(top_left_warp[1])
        warp_x2,warp_y2 = (bot_right_warp[0]),(bot_right_warp[1])
        
        x,y = np.linspace(x1, x2, 86),np.linspace(y1, y2, 35)
        warp_x,warp_y = np.linspace(warp_x1,warp_x2,86),np.linspace(warp_y1,warp_y2,35)
#        x,y = np.arange(x1,x2,1),np.arange(y1,y2,1)
#        warp_x,warp_y = np.arange(warp_x1,warp_x2,1),np.arange(warp_y1,warp_y2,1)
        
        xx,yy = np.meshgrid(x,y)
        warp_xx,warp_yy = np.meshgrid(warp_x,warp_y)
        
        It1_interpolate = It1_spline.ev(yy,xx)
        Itn_interpolate = Itn_spline.ev(warp_yy,warp_xx)

        err = It1_interpolate - Itn_interpolate
        
        Grad_x = Grad_x_spline.ev(warp_yy,warp_xx).ravel().reshape(-1,1)
        Grad_y = Grad_y_spline.ev(warp_yy,warp_xx).ravel().reshape(-1,1)

        Grad = np.concatenate((Grad_x,Grad_y),axis=1)
        
        Steepest_direction = Grad @ Jacobian_W
        Total_err = Steepest_direction.T @ err.ravel().reshape(-1,1)
        Hessian = Steepest_direction.T @ Steepest_direction
        delta_p = np.linalg.inv(Hessian) @ Total_err
        delta_p_l2 = np.sum(delta_p**2)
        
        p[0] += delta_p[0]
        p[1] += delta_p[1]
       
    return p




frames = np.load('../data/carseq.npy')

x1,y1,x2,y2 = 59,116,145,151

num_frames = np.shape(frames)[2]
rects = np.zeros((num_frames,4))
rects_prime = np.zeros((num_frames,4))
It_first = frames[:,:,0]#first frame
rects[0,:] = np.array([x1,y1,x2,y2])
rects_prime[0,:] = np.array([x1,y1,x2,y2])
rect1 = np.array([x1,y1,x2,y2])

for i in range(num_frames-1):
    It = frames[:,:,i]
    It1 = frames[:,:,i+1]
    rect = rects[i,:] 
    [x1,y1,x2,y2] = rects[i,:]
    
    pn = LucasKanade(It, It1, rect, p0 = np.zeros(2))
    
    x1_temp,y1_temp,x2_temp,y2_temp = np.floor(x1+pn[0]),np.floor(y1+pn[1]),np.floor(x2+pn[0]),np.floor(y2+pn[1])
    rect_temp = np.array([x1_temp,y1_temp,x2_temp,y2_temp]).T
    
    p_prime = LucasKanade_1_to_n(It_first, It1, pn, rect1, rect_temp)
    
    if sum(np.abs(p_prime - pn)) > 4:
        x1,y1,x2,y2 = np.floor(x1_temp+p_prime[0]),np.floor(y1_temp+p_prime[1]),np.floor(x2_temp+p_prime[0]),np.floor(y2_temp+p_prime[1])
        rect_prime = np.array([x1,y1,x2,y2]).T
    else:
        x1,y1,x2,y2 = x1_temp,y1_temp,x2_temp,y2_temp
        rect_prime = np.array([x1,y1,x2,y2]).T
        
    if i % 100 == 0:
        plt.figure()
        ax1 = plt.gca()
        ax1.add_patch(patches.Rectangle([x1_temp,y1_temp],width=x2_temp-x1_temp,height=y2_temp-y1_temp,fill=None,color='r'))
        ax1.add_patch(patches.Rectangle([x1,y1],width=x2-x1,height=y2-y1,fill=None,color='g'))
        plt.imshow(It1,cmap='gray')
    plt.show()
    
    rects[i+1,:] = rect_temp.T
    rects_prime[i+1,:] = rect_prime.T
    print(rect_prime.T)
    
np.save('carseqrects-wcrt.npy',rects_prime) # template correction