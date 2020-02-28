import numpy as np
from scipy.interpolate import RectBivariateSpline

def InverseCompositionAffine(It, It1):
	# Input: 
	#	It: template image
	#	It1: Current image

	# Output:
	#	M: the Affine warp matrix [2x3 numpy array]

    # put your implementation here
    M = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    p = np.zeros(6)
    num_row = np.shape(It)[0]
    num_col = np.shape(It)[1]
    
    x1,y1 = 0,0 #top left corner
    x2,y2 = num_col,num_row #bottom right corner
    top_left = np.array([x1,y1,1]).T
    bot_right = np.array([x2,y2,1]).T
    
    threshold = 10
    count = 0
    max_count = 100
    delta_p_l2 = 100
    delta_p = np.ones((2,3))

    Grad_y,Grad_x = np.gradient(It)#calculate the gradiant of template
    It_spline = RectBivariateSpline(np.arange(num_row),np.arange(num_col),It)
    It1_spline = RectBivariateSpline(np.arange(num_row),np.arange(num_col),It1)
    

    Grad = np.hstack((Grad_x.T,Grad_y.T)).reshape(num_row*num_col,2)


    
    while np.linalg.norm(delta_p) > threshold and count < max_count:
        count += 1
        #warp orginal coordinate
        M = np.array([[1+p[0],p[1],  p[2]],
                      [p[3],  1+p[4],p[5]]]) # warp matrix
        
        top_left_warp = M @ top_left
        bot_right_warp = M @ bot_right
        warp_x1,warp_y1 = np.floor(top_left_warp[0]),np.floor(top_left_warp[1])
        warp_x2,warp_y2 = np.floor(bot_right_warp[0]),np.floor(bot_right_warp[1])
       
        x,y = np.arange(x1,x2,1),np.arange(y1,y2,1)
        warp_x,warp_y = np.arange(warp_x1,warp_x2,1),np.arange(warp_y1,warp_y2,1)
        
        xx,yy = np.meshgrid(x,y)
        warp_xx,warp_yy = np.meshgrid(warp_x,warp_y)
        
        It_interpolate = It_spline.ev(yy,xx)
        It1_interpolate = It1_spline.ev(warp_yy,warp_xx)

        err = It_interpolate - It1_interpolate
        #    Jacobian_M = np.zeros((2,6,num_col*num_row))
        Steepest_direction = np.zeros((num_row*num_col,6))
        for i in range(num_col):
            for j in range(num_row):
                Jacobian_M = np.array([[i,0,j,0,1,0],
                                   [0,i,0,j,0,1]]) # jacobian matrix of W
                Steepest_direction[j*num_col+i,:] = Grad[j*num_col+i,:] @ Jacobian_M #  Steepest_direction  for each point
    

    
        Hessian = Steepest_direction.T @ Steepest_direction
                
        Total_err = Steepest_direction.T @ err.ravel().reshape(-1,1)
        
        delta_p = np.linalg.inv(Hessian) @ Total_err
#        delta_p_l2 = np.sum(delta_p**2)
#        
        delta_p = delta_p.reshape(2,3)
        delta_p = np.vstack((delta_p,np.array([0,0,1])))
        M = M @ np.linalg.inv(delta_p)
        

       
    
    
    return M
