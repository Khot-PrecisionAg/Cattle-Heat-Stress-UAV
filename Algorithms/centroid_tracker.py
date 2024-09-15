from collections import OrderedDict
import numpy as np
from scipy.spatial import distance as dist

class CentroidTracker:
    """
    A class used to track objects (e.g., cattle) in video frames based on their centroids.
    
    This tracker assigns unique IDs to objects, tracks their positions over time, 
    and handles objects that disappear from frames by removing them after a 
    specified number of frames.

    Attributes
    ----------
    maxDisappeared : int
        Maximum number of consecutive frames an object can be missing before it is deregistered.
    nextObjectID : int
        The next unique object ID to be assigned.
    objects : OrderedDict
        A dictionary that stores the object ID and its centroid.
    disappeared : OrderedDict
        A dictionary that tracks how many consecutive frames each object has been missing.
    """

    def __init__(self, maxDisappeared=50):
        """
        Initializes the CentroidTracker with an optional maxDisappeared parameter.

        Parameters
        ----------
        maxDisappeared : int, optional
            Number of frames to allow an object to be missing before deregistering (default is 50).
        """
        self.nextObjectID = 0  # The next unique ID to assign to an object
        self.objects = OrderedDict()  # Stores the objects' centroids
        self.disappeared = OrderedDict()  # Tracks the number of frames an object has been missing
        self.maxDisappeared = maxDisappeared  # Maximum allowed frames before deregistering an object

    def register(self, centroid):
        """
        Registers a new object with a unique ID and initializes its centroid.

        Parameters
        ----------
        centroid : tuple
            The (x, y) coordinates of the object's centroid.
        """
        self.objects[self.nextObjectID] = centroid
        self.disappeared[self.nextObjectID] = 0  # Initialize disappearance counter
        self.nextObjectID += 1  # Increment the next available object ID

    def deregister(self, objectID):
        """
        Deregisters an object by removing it from the tracking dictionaries.

        Parameters
        ----------
        objectID : int
            The ID of the object to be removed.
        """
        del self.objects[objectID]
        del self.disappeared[objectID]

    def update(self, rects):
        """
        Updates the tracker with new bounding box rectangles, registering new objects and 
        updating existing ones. If an object disappears, increments its disappearance counter.

        Parameters
        ----------
        rects : list
            A list of bounding boxes (startX, startY, endX, endY) for each detected object.

        Returns
        -------
        objects : OrderedDict
            Updated dictionary of object IDs and their centroids.
        """
        # If no rectangles are provided, mark existing objects as disappeared
        if len(rects) == 0:
            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] += 1
                # If the disappearance count exceeds the maximum, deregister the object
                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)
            return self.objects

        # Initialize an array to hold the centroids for the input rectangles
        inputCentroids = np.zeros((len(rects), 2), dtype="int")

        # Calculate the centroid for each rectangle
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            cX = int((startX + endX) / 2.0)  # X-coordinate of the centroid
            cY = int((startY + endY) / 2.0)  # Y-coordinate of the centroid
            inputCentroids[i] = (cX, cY)  # Store centroid

        # If no objects are currently being tracked, register each new centroid
        if len(self.objects) == 0:
            for i in range(len(inputCentroids)):
                self.register(inputCentroids[i])

        else:
            # Get the current object IDs and centroids
            objectIDs = list(self.objects.keys())
            objectCentroids = list(self.objects.values())

            # Compute the distance between each pair of object centroids and input centroids
            D = dist.cdist(np.array(objectCentroids), inputCentroids)

            # Find the minimum distance and sort rows by that minimum
            rows = D.min(axis=1).argsort()

            # Find the column index with the smallest value for each row
            cols = D.argmin(axis=1)[rows]

            # Track which rows and columns have already been matched
            usedRows = set()
            usedCols = set()

            # Loop over the (row, col) index pairs
            for (row, col) in zip(rows, cols):
                # Ignore if the row or column has already been matched
                if row in usedRows or col in usedCols:
                    continue

                # Otherwise, update the object centroid and reset disappearance counter
                objectID = objectIDs[row]
                self.objects[objectID] = inputCentroids[col]
                self.disappeared[objectID] = 0

                # Mark the row and column as used
                usedRows.add(row)
                usedCols.add(col)

            # Determine which object centroids or input centroids were unmatched
            unusedRows = set(range(D.shape[0])).difference(usedRows)
            unusedCols = set(range(D.shape[1])).difference(usedCols)

            # For any unmatched existing objects, increment the disappearance count
            if D.shape[0] >= D.shape[1]:
                for row in unusedRows:
                    objectID = objectIDs[row]
                    self.disappeared[objectID] += 1
                    # If an object has disappeared for too long, deregister it
                    if self.disappeared[objectID] > self.maxDisappeared:
                        self.deregister(objectID)

            # Register any unmatched input centroids as new objects
            else:
                for col in unusedCols:
                    self.register(inputCentroids[col])

        return self.objects
