import numpy as np
import cv2

# Function to select points on the image using left-click
def select_points(event, x, y, flags, params):
    global point_index, image_points
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img_copy, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Select Points", img_copy)
        image_points.append((x, y))
        point_index += 1
        if point_index == 4:
            cv2.destroyAllWindows()

# Load the image
image_path = "your_image_path.jpg"
img = cv2.imread(image_path)
img_copy = img.copy()

# Display the image and allow user to select points
point_index = 0
image_points = []
cv2.namedWindow("Select Points")
cv2.setMouseCallback("Select Points", select_points)
cv2.imshow("Select Points", img_copy)
cv2.waitKey(0)

# Convert selected points to numpy array
image_points = np.array(image_points)

# Corresponding world points (assuming a square unit)
world_points = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=np.float32)

# Step 1: Estimate the image-to-world homography matrix H
H, _ = cv2.findHomography(image_points, world_points, cv2.RANSAC)

# Step 2: Back-project each image point into the world plane via homography
image_points_float32 = image_points.astype(np.float32)  # Convert to float32 datatype
world_points_homogeneous = cv2.perspectiveTransform(image_points_float32.reshape(-1, 1, 2), H)

# Step 3: Compute the Euclidean distances between pairs of world points
distances = np.sqrt(np.sum(np.diff(world_points_homogeneous.squeeze(), axis=0)**2, axis=1))

# Print the estimated homography matrix and distances
print("Estimated Homography Matrix:")
print(H)
print("Euclidean distances between the selected points in the world plane:")
for i, distance in enumerate(distances):
    print(f"Distance between X{i+1} and X{i+2 if i < 3 else 1}: {distance:.2f}")

# Draw the selected points on the image
for point in image_points:
    cv2.circle(img, tuple(point), 5, (0, 255, 0), -1)

# Display the image with selected points
cv2.imshow("Selected Points", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
