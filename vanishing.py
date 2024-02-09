import math
import cv2
import numpy as np
import matplotlib.pyplot as plt

from utils import show


REJECT_DEGREE_TH = 4.0


def filter_lines(lines):
    out_lines = []

    for Line in lines:
        [[x1, y1, x2, y2]] = Line

        # Calculating equation of the line: y = mx + c
        m = (y2 - y1) / (x2 - x1)
        c = y1 - m * x1
        # theta from SLOPE
        theta = math.degrees(math.atan(m))

        # Rejecting lines of slope near to 0 degree or 90 degree and storing others
        if REJECT_DEGREE_TH <= abs(theta) <= (90 - REJECT_DEGREE_TH):
            l_ = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            out_lines.append([x1, y1, x2, y2, m, c, l_])

    # Removing extra lines
    # (we might get many lines, so we are going to take only longest 15 lines
    # for further computation because more than this number of lines will only
    # contribute towards slowing down of our algo.)
    if len(out_lines) > 15:
        out_lines = sorted(out_lines, key=lambda x: x[-1], reverse=True)
        out_lines = out_lines[:15]

    return out_lines


def intersection_of_lines(m1, c1, m2, c2):
    x = (c1 - c2) / (m2 - m1)
    y = m1 * x + c1
    return x, y


def __get_vanishing_point_from_lines(lines):
    # vanishing_point = (0, 0)
    # min_error = int(1e8)
    vanishing_points = {}

    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            m1, c1 = lines[i][4], lines[i][5]
            m2, c2 = lines[j][4], lines[j][5]

            intersection = intersection_of_lines(m1, c1, m2, c2)

            err = 0
            for k in range(len(lines)):
                # m, c = lines[k][4], lines[k][5]
                x0, y0 = intersection
                x1, y1, x2, y2 = lines[k][:4]

                # Calculating distance of point(x0, y0) from line
                d = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 -
                        y2 * x1) / math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)

                err += d ** 2

            err = math.sqrt(err)

            if err < int(1e8):
                vanishing_points[tuple(intersection)] = err
            #     min_error = err
            #     vanishing_point = intersection
            # vanishing_points[tuple(intersection)] = err

    return vanishing_points


def get_vanishing_points(image):
    original_image = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurGray = cv2.GaussianBlur(gray, (5, 5), 1)
    # Generating Edge image
    edgeGray = cv2.Canny(blurGray, 40, 255)

    # Finding Lines in the image
    lines = cv2.HoughLinesP(edgeGray, 1, np.pi / 180, 50, 10, 15)
    for line in np.squeeze(lines):
        cv2.line(image, (line[0], line[1]), (line[2], line[3]), (0, 255, 0), 2)
    show(image)

    lines = filter_lines(lines)
    for x1, y1, x2, y2, m, c, l in np.squeeze(lines):
        cv2.line(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    point = __get_vanishing_point_from_lines(lines)
    return point
    cv2.circle(image, (int(point[0]), int(point[1])), 10, (0, 0, 255), -1)
    return image


def try_multi_vanishing_lines(image):
    image = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    canny_thresholds = [(50, 150), (100, 200), (150, 250)]
    hough_params = [(50, 5, 5), (100, 10, 10), (150, 15, 15)]

    fig, axes = plt.subplots(len(canny_thresholds),
                             len(hough_params), figsize=(12, 9))

    for i, canny_params in enumerate(canny_thresholds):
        for j, hough_params_single in enumerate(hough_params):
            canny = cv2.Canny(gray, canny_params[0], canny_params[1])

            lines = cv2.HoughLinesP(
                canny, rho=1,
                theta=np.pi/180,
                threshold=hough_params_single[0],
                minLineLength=hough_params_single[1],
                maxLineGap=hough_params_single[2]
            )

            image_copy = np.copy(image)

            if lines is not None:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    cv2.line(image_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)

            axes[i, j].imshow(cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB))
            axes[i, j].set_title(
                f"Canny: {canny_params}, Hough: {hough_params_single}")
            axes[i, j].axis('off')

    plt.tight_layout()
    plt.show()
