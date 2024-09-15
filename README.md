# Cattle-Heat-Stress-UAV

This repository contains algorithms and results for monitoring cattle heat stress using UAV-based thermal and RGB video. The project leverages image processing techniques to detect and track cattle in real-time, estimate body surface temperatures (BST), and provide automated heat stress monitoring.

## Algorithms

The repository includes the following algorithms located in the /Algorithms/ directory:
1. centroid_tracker.py

This script implements a Centroid Tracker using a combination of Mask R-CNN and Centroid Tracking Algorithm to detect and track individual cows in thermal and RGB video frames. The tracker registers, updates, and tracks the centroids of cows, ensuring real-time monitoring even when cows disappear from the frame temporarily.
Key Functions:

    register(centroid): Registers a new object (cow) in the system with its centroid.
    deregister(objectID): Removes a cow that has disappeared beyond a specified threshold.
    update(rects): Updates the position of tracked cows based on new input from the UAV video frames.

2. undistortion_algorithm.py

This algorithm provides a method to undistort thermal-RGB images captured by UAVs. It utilizes camera calibration matrices (intrinsic and distortion coefficients) to correct for image distortion caused by the UAV's camera.
Key Functions:

    undis(cv_img): Takes the input image, applies undistortion using the camera calibration matrix, and returns the corrected image along with its dimensions.

Results

Processed thermal and RGB images can be found in the /Results/ directory. These results demonstrate successful cow detection in both types of imagery.
Results Folder:

    Detected cows in thermal and RGB images for various test scenarios.

Usage

    Centroid Tracker:
        To use the centroid tracker, run centroid_tracker.py with your video input to track cows and analyze their positions over time.

    Undistortion Algorithm:
        Use undistortion_algorithm.py to correct image distortion in thermal-RGB imagery from UAV footage before performing further analysis.

Acknowledgments

This project was developed by by Keshawa M. Dadallage from WSU Precision Agriculture group.
License

This project is licensed under the Creative Commons Attribution (CC BY) license. Please refer to LICENSE for more details.
