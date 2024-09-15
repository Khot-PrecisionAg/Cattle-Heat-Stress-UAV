#Algorithm 2 

def undis(cv_img): 

    # Use the provided K and d matrices directly from the image 

    K = np.array([[7.653e+02, 0, 3.154e+02], 

                  [0, 7.653e+02, 2.559e+02], 

                  [0, 0, 1]]) 

    d = np.array([-3.596e-01, 1.739e-01, 7.411e-05, 9.025e-05, -1.927e-01]) 

    h, w = cv_img.shape[:2] 

    newcam, roi = cv2.getOptimalNewCameraMatrix(K, d, (w, h), 1, (w, h)) 

    dest = cv2.undistort(cv_img, K, d, None, newcam) 

    x, y, w, h = roi 

    dest = dest[y:y + h, x:x + w] 

    height, width, channels = dest.shape 

    dim = (width, height) 

    return dest, dim 
