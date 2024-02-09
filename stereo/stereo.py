import cv2
import matplotlib.pyplot as plt
from pathlib import Path

from .config import StereoImageConfig
from utils import show


def read_image(conf: StereoImageConfig, should_show: bool = False):
    assert isinstance(conf, StereoImageConfig), 'Invalid configuration'
    path = Path(__file__).parent / f'./images/{conf.filename}'
    full_stereo = cv2.imread(str(path))
    if full_stereo is None:
        raise FileNotFoundError(f"Image {conf.filename} not found")
    stereoL = full_stereo[:, :(full_stereo.shape[1]//2)+conf.lOffset]
    stereoR = full_stereo[:, (full_stereo.shape[1]//2)-conf.rOffset:]
    if should_show:
        show(full_stereo)
        show(stereoL)
        show(stereoR)
    return stereoL, stereoR


def show_disparity(stereoL, stereoR, blockSize=15):
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=blockSize)
    disparity = stereo.compute(cv2.cvtColor(
        stereoL, cv2.COLOR_BGR2GRAY), cv2.cvtColor(stereoR, cv2.COLOR_BGR2GRAY))
    plt.imshow(disparity, 'gray')
    plt.show()


def merge_images(stereo_image_left, stereo_image_right, blockSize=15):
    # Convert the stereo images to grayscale
    stereo_image_left = cv2.cvtColor(
        cv2.Canny(stereo_image_left, 100, 200), cv2.COLOR_GRAY2BGR)
    stereo_image_right = cv2.cvtColor(
        cv2.Canny(stereo_image_right, 100, 200), cv2.COLOR_GRAY2BGR)
    stereo_image_left_gray = cv2.cvtColor(
        stereo_image_left, cv2.COLOR_BGR2GRAY)
    stereo_image_right_gray = cv2.cvtColor(
        stereo_image_right, cv2.COLOR_BGR2GRAY)

    # Create a StereoBM object
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=blockSize)

    # Compute the disparity map
    disparity_map = stereo.compute(
        stereo_image_left_gray, stereo_image_right_gray)

    # Normalize the disparity map to the range [0, 255]
    normalized_disparity_map = cv2.normalize(
        disparity_map, None,
        alpha=0, beta=255,
        norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U
    )

    # Convert the grayscale disparity map to color
    colored_disparity_map = cv2.applyColorMap(
        normalized_disparity_map, cv2.COLORMAP_JET)

    # Display the merged image
    plt.imshow(colored_disparity_map)
    plt.axis('off')
    plt.show()


def display_mean_image(stereoL, stereoR):
    gstereoL, gstereoR = cv2.cvtColor(
        stereoL, cv2.COLOR_BGR2GRAY), cv2.cvtColor(stereoR, cv2.COLOR_BGR2GRAY)
    mean = (gstereoL + gstereoR) / 2
    plt.imshow(mean, 'gray')
    plt.show()


def display_image_difference(stereoL, stereoR):
    gstereoL, gstereoR = cv2.cvtColor(
        stereoL, cv2.COLOR_BGR2GRAY), cv2.cvtColor(stereoR, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gstereoL, gstereoR)
    plt.imshow(diff, 'gray')
    plt.show()
