import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('./test-images/ILSVRC2016_test_00004783.JPEG')

grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT();
kp, des = sift.detectAndCompute(grey, None);

img = cv2.drawKeypoints(grey, kp, flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

for keypoint in kp:
    print keypoint.pt, keypoint.size

cv2.imwrite('sift_keypoints.jpg', img)
plt.figure(1)
plt.imshow(img)

# Create SURF boject, with Hessian threshold of 400
surf = cv2.SURF(4000)
kp, des = surf.detectAndCompute(img, None)
img2 = cv2.drawKeypoints(img, kp, None, (255, 0, 0), 4)
plt.figure(2)
plt.imshow(img2)
#plt.show()

