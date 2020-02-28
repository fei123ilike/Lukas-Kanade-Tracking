import numpy as np
from scipy.interpolate import RectBivariateSpline

def LucasKanadeBasis(It, It1, rect, bases):
	# Input: 
	#	It: template image
	#	It1: Current image
	#	rect: Current position of the car
	#	(top left, bot right coordinates)
	#	bases: [n, m, k] where nxm is the size of the template.
	# Output:
	#	p: movement vector [dp_x, dp_y]

    # Put your implementation here
    p = np.zeros(2)
    
    bases_num = np.shape(bases)[2]
    bases_width = np.shape(bases)[1]
    bases_height = np.shape(bases)[0]
#    bases_reshape = bases.reshape(bases_height*bases_width,bases_num)
    bases_reshape = bases.reshape(-1,bases_num)
#    bases_sum = bases_reshape @ bases_reshape.T # compute the matrix here(instead of scalar), that is why it is slow
    
    bases_sum = 0
    for i in range(bases_num):
        bases_sum += bases_reshape[:,i] @ bases_reshape[:,i].T
    c = 1 - bases_sum #coeeficcient for bases, just a scalar

    
    x1,y1 = rect[0],rect[1] #top left corner
    x2,y2 = rect[2],rect[3] #bottom right corner
    top_left = np.array([x1,y1,1]).T
    bot_right = np.array([x2,y2,1]).T
    
    threshold = 0.01 
    count = 0
    max_count = 100
    delta_p_l2 = 100
    num_row = np.shape(It)[0]
    num_col = np.shape(It)[1]

    Grad_It1_y,Grad_It1_x = np.gradient(It1)
    It_spline = RectBivariateSpline(np.arange(num_row),np.arange(num_col),It)
    It1_spline = RectBivariateSpline(np.arange(num_row),np.arange(num_col),It1)
    
    Grad_x_spline = RectBivariateSpline(np.arange(num_row),np.arange(num_col),Grad_It1_x)
    Grad_y_spline = RectBivariateSpline(np.arange(num_row),np.arange(num_col),Grad_It1_y)
    
    
    while delta_p_l2 > threshold and count < max_count:
        count += 1
        #warp orginal coordinate
        W = np.array([[1,0,p[0]],
                      [0,1,p[1]]]) # warp matrix
        Jacobian_W = np.array([[1,0],
                               [0,1]]) # jacobian matrix of W
        top_left_warp = W @ top_left
        bot_right_warp = W @ bot_right
        warp_x1,warp_y1 = np.floor(top_left_warp[0]),np.floor(top_left_warp[1])
        warp_x2,warp_y2 = np.floor(bot_right_warp[0]),np.floor(bot_right_warp[1])
       
#        x,y = np.linspace(x1, x2, 55),np.linspace(y1, y2, 47)
#        warp_x,warp_y = np.linspace(warp_x1,warp_x2,55),np.linspace(warp_y1,warp_y2,47)
        x,y = np.arange(x1,x2,1),np.arange(y1,y2,1)
        warp_x,warp_y = np.arange(warp_x1,warp_x2,1),np.arange(warp_y1,warp_y2,1)
        
        xx,yy = np.meshgrid(x,y)
        warp_xx,warp_yy = np.meshgrid(warp_x,warp_y)
        
        
        
        It_interpolate = It_spline.ev(yy,xx)
        It1_interpolate = It1_spline.ev(warp_yy,warp_xx)
 
        err = It_interpolate - It1_interpolate
        
        Grad_x = Grad_x_spline.ev(warp_yy,warp_xx).ravel().reshape(-1,1)
        Grad_y = Grad_y_spline.ev(warp_yy,warp_xx).ravel().reshape(-1,1)
        Grad = np.concatenate((Grad_x,Grad_y),axis=1)
        Steepest_direction = Grad @ Jacobian_W
        
        #||Bz||**2 ||(1 - BBTz)*Steepeest_derection - (1 - BBTz)*err ||**2

        Bz =  c * Steepest_direction
        Total_err = Bz.T @ (c * err.ravel().reshape(-1,1))
        
#        Bz =  Steepest_direction - bases_sum @ Steepest_direction
#        Total_err = Bz.T @ (err.ravel().reshape(-1,1))
        Hessian = Bz.T @ Bz
#        print('.............')
#        print(Hessian)
        

        delta_p = np.linalg.inv(Hessian) @ Total_err
        delta_p_l2 = np.sum(delta_p**2)
       
        p[0] += delta_p[0]
        p[1] += delta_p[1]
       
    return p
    

    
