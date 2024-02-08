import cv2
import numpy as np

# Load the image
image_path = "test_image.jpg"
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply automatic Canny edge detection
canny = cv2.Canny(gray, 50, 150)

# Perform Hough line detection to obtain straight lines
lines = cv2.HoughLinesP(canny, rho=1, theta=np.pi/180, threshold=100, minLineLength=50, maxLineGap=5)

# Draw the detected lines on the original image
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Display the original image with detected lines
cv2.imshow("Detected Lines", image)
cv2.waitKey(0)
cv2.destroyAllWindows()