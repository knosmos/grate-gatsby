import cv2
import numpy as np

def warp(img_f, shear_v):
    img = cv2.imread(img_f)
    h, w, _ = img.shape
    M = np.array([[1, 0, 0], [shear_v, 1, 0]], dtype=np.float32)
    warped = cv2.warpAffine(img, M[:2], (w, h))
    return warped

cv2.imwrite("diff1_corrected.png", warp("diff1.png", 0.22))
cv2.imwrite("diff2_corrected.png", warp("diff2.png", 0.22))