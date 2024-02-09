# Dos Locos

_(two crazies)_


> **Computer Vision Project**
>
> 3D Reconstruction of Renaissance paintings using Single View Metrology
>
> _Under the guidance of Dr. Raghavendra Singh and Rashmi Nagpal_

## Team

- P2023PTLP0044 - **Lokesh Arora** ([@lokeshtlp](https://github.com/lokeshtlp))
- P2023PTLP0036 - **Rajat Abraham Jacob** ([@RajatJacob](https://github.com/RajatJacob))

## Usage

```bash
sh setup.sh
```


Run the setup script to initialise the environment. This may take a while. We used Poetry to handle any dependency conflicts.

Once the dependencies are installed, the [`main.ipynb`](main.ipynb) notebook would be a good starting point.

## Introduction

This repository implements algorithms described in the paper "Single-View Metrology: Algorithms and Applications" by Antonio Criminisi. These algorithms aim to extract three-dimensional geometric information from a single, uncalibrated image of a scene.

The paper addresses the challenge of extracting three-dimensional geometric information from a single, uncalibrated image. Divided into two parts, the paper first introduces basic algorithms for reconstructing scene geometry from single perspective images. It then explores various applications of single-view metrology in disciplines such as architecture, history of art, and forensic science. Additionally, techniques for enhancing the automation of the reconstruction process are discussed, accompanied by practical examples illustrating the efficacy of the proposed methods.
Key Algorithms

1. Planar Measurements

This algorithm allows for the measurement of lengths of segments on planar surfaces in an image. It involves estimating an image-to-world homography matrix, which maps points on the image plane to corresponding points on the world plane. Once the homography matrix is known, distances between world points can be extracted, enabling the reconstruction of planar surfaces.

2. Height Computation from Single Images

The height computation algorithm focuses on estimating the height of objects relative to a reference plane using single images. It involves estimating the vanishing point for the vertical direction and the vanishing line of the reference plane. By selecting top and base points of the reference segment and applying a metric factor, the height of objects can be computed from image quantities only, without the need for camera calibration.

3. Object Segmentation by Interactive Silhouette Cut-Out

This algorithm facilitates the segmentation of objects within a scene by interactively extracting their silhouettes from images. It employs a dynamic programming-type approach, where the problem of estimating the contour between two user-specified points is framed as finding the optimal path between them. The technique utilizes normalized cross-correlation measures to constrain the extracted contour, enabling precise object segmentation.

## References
- [Criminisi, Antonio, Ian Reid, and Andrew Zisserman. "Single view metrology." International Journal of Computer Vision 40 (2000): 123-148.](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=78c666b244a85c0e9ca2418321e985e2d6766966)
- [Criminisi, A., 2001. Accurate visual metrology from single and multiple uncalibrated images. Springer Science & Business Media.](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/criminisi_phdthesis.pdf)
- https://github.com/LiheYoung/Depth-Anything
