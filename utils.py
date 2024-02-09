import cv2
import numpy as np
import matplotlib.pyplot as plt


def show(image):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()


def edges(image):
    image = image.copy()
    image = cv2.GaussianBlur(image, (0, 0), 5)
    return image - cv2.GaussianBlur(image, (0, 0), 5)


def viterbi_object_segmentation(image, ksize=5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)

    gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)

    mask = np.zeros_like(gradient_magnitude, dtype=np.uint8)
    mask[gradient_magnitude > 127] = 255

    result = cv2.bitwise_and(image, image, mask=mask)

    return result
