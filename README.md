# Cattle-Heat-Stress-UAV

This repository contains algorithms and results for monitoring cattle heat stress using UAV-based thermal and RGB video. The project leverages image processing techniques to detect and track cattle in real-time, estimate body surface temperatures (BST), and provide automated heat stress monitoring.

## Algorithms

The repository includes the following algorithms located in the /Algorithms/ directory:
1. centroid_tracker.py

The Centroid Tracker algorithm effectively tracks individual cows in thermal and RGB video frames captured by UAVs, preventing duplicate identification. This is crucial for real-time video streams, as duplicated identification can occur due to the nature of waypoint navigation systems.

The algorithm assigns unique identifiers (IDs) to each cow detected by the instance segmentation model, tracking their movement across consecutive frames. It uses a distance matrix to match cow centroids between frames, ensuring accurate tracking without duplicate counting. The centroid tracker adapts to dynamic settings in large feedlots, adjusting for occlusions and movement.

Key Features:

    Prevents duplicate cow identification across frames.
    Assigns unique IDs to cows and tracks their movements in real-time.
    Ensures accurate and continuous monitoring in large-scale drylot environments.

Process:

    Calculates centroids of bounding boxes from segmentation model outputs.
    Uses a distance matrix and linear assignment algorithm to match centroids between frames.
    Registers new cows and deregisters those absent for an extended duration.
    Ensures reliable tracking and prevents duplicates.

2. undistortion_algorithm.py

This algorithm provides a thermal image distortion correction method. It addresses radial distortion in UAV thermal images due to wide-angle lenses by using camera calibration parameters. The corrected images are then used for further processing, such as body surface temperature extraction.

Thermal images were corrected using the camera matrix and distortion coefficients obtained from calibration. The algorithm ensures that the thermal images align correctly with RGB data for accurate pixel-level mapping when using a combined approach.

Key Features:

    Corrects thermal image distortion caused by wide-angle lenses.
    Uses pre-calibrated camera matrices and distortion coefficients.
    Ensures proper alignment for pixel-to-pixel mapping between RGB and thermal images.

Results

The /Results/ folder contains the processed thermal and RGB for cow detection and tracking in real-time video streams.

Results Folder:

    Detected cows in thermal and RGB images.

Usage

    Centroid Tracker:
        To use the centroid tracker, run centroid_tracker.py with your video input to track cows and 
        analyze their positions over time.

    Undistortion Algorithm:
        Use undistortion_algorithm.py to correct image distortion in thermal-RGB imagery from 
        UAV video before performing further analysis.

Acknowledgments

This project was developed by by Keshawa M. Dadallage from WSU Precision Agriculture group.

License

This project is licensed under the Creative Commons Attribution (CC BY) license. Please refer to LICENSE for more details.
