import cv2
import numpy as np

def undis(cv_img):
    """
    Corrects radial distortion in a given image using pre-calibrated camera matrix (K) 
    and distortion coefficients (d). Returns the undistorted image and its dimensions.

    Parameters
    ----------
    cv_img : numpy.ndarray
        The distorted image captured from the camera (RGB or thermal).

    Returns
    -------
    dest : numpy.ndarray
        The undistorted image after applying distortion correction.
    dim : tuple
        A tuple containing the width and height of the undistorted image.
    """

    # Camera matrix (K) and distortion coefficients (d) obtained through calibration
    K = np.array([[7.653e+02, 0, 3.154e+02],  # Focal lengths and optical center
                  [0, 7.653e+02, 2.559e+02],
                  [0, 0, 1]])

    d = np.array([-3.596e-01, 1.739e-01, 7.411e-05, 9.025e-05, -1.927e-01])  # Distortion coefficients

    # Get image dimensions
    h, w = cv_img.shape[:2]

    # Compute optimal new camera matrix and region of interest (ROI) for undistortion
    newcam, roi = cv2.getOptimalNewCameraMatrix(K, d, (w, h), 1, (w, h))

    # Apply undistortion to the input image
    dest = cv2.undistort(cv_img, K, d, None, newcam)

    # Crop the image based on the ROI
    x, y, w, h = roi
    dest = dest[y:y + h, x:x + w]

    # Get final dimensions of the undistorted image
    height, width, channels = dest.shape
    dim = (width, height)

    return dest, dim
