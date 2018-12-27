import cv2
import numpy as np
def expand(img):

    row, column = img.shape[0], img.shape[1]
    print("row = {}, column = {}".format(row, column))

    pts1 = np.float32([[280,0],[0,row],[380,0],[column,row]])
    pts2 = np.float32([[0,0],[0,row],[column,0],[column,row]])

    M = cv2.getPerspectiveTransform(pts1,pts2)

    expanded = cv2.warpPerspective(img,M,(int(column),int(row)))
    
    return expanded
