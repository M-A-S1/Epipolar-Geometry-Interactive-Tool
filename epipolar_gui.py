import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

# Global variables
img1, img2 = None, None
F_7, F_8 = None, None  # Fundamental Matrices
fig, ax1, ax2 = None, None, None  # Matplotlib figure and axes

def compute_fundamental_matrices():
    """Computes the fundamental matrices using 7-point and 8-point algorithms."""
    global img1, img2, F_7, F_8

    # Convert images to grayscale for feature detection
    gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)

    # Initialize SIFT detector
    sift = cv2.SIFT_create()

    # Detect keypoints and compute descriptors for both images
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)

    # FLANN parameters for matching descriptors
    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Match descriptors using FLANN matcher
    matches = flann.knnMatch(des1, des2, k=2)

    # Apply Lowe's ratio test to filter good matches
    good_matches = sorted([m for m, n in matches if m.distance < 0.7 * n.distance], key=lambda x: x.distance)
    if len(good_matches) < 7:
        print("Not enough matches found.")
        return

    # Use only top 7 and top 8 correspondences
    pts1_7 = np.float32([kp1[m.queryIdx].pt for m in good_matches[:7]])
    pts2_7 = np.float32([kp2[m.trainIdx].pt for m in good_matches[:7]])
    pts1_8 = np.float32([kp1[m.queryIdx].pt for m in good_matches[:8]])
    pts2_8 = np.float32([kp2[m.trainIdx].pt for m in good_matches[:8]])

    # Compute Fundamental Matrices
    F_7_all, _ = cv2.findFundamentalMat(pts1_7, pts2_7, cv2.FM_7POINT)      # 7-point algorithm
    F_8, _ = cv2.findFundamentalMat(pts1_8, pts2_8, cv2.FM_8POINT)          # 8-point algorithm (for more or equal points other robust methods: cv2.FM_LMEDS, cv2.FM_RANSAC)

    # Handle the case where multiple matrices are returned by the 7-point algorithm
    if F_7_all is not None:
        if F_7_all.ndim == 2:  # Single matrix case
            F_7 = F_7_all
        elif F_7_all.ndim == 3:  # Multiple matrices returned
            F_7 = F_7_all[:, :, 0]  # Choose the first fundamental matrix
        print("7-Point Fundamental Matrix Computed Successfully!")
    if F_8 is not None:
        print("8-Point Fundamental Matrix Computed Successfully!")

def draw_epipolar_lines(event):
    """Draws epipolar lines from both algorithms in different colors."""
    global img1, img2, F_7, F_8, fig, ax1, ax2

    if F_7 is None or F_8 is None:
        print("Fundamental matrices not computed yet.")
        return

    x, y = event.xdata, event.ydata
    if x is None or y is None:
        return

    pt1_hom = np.array([x, y, 1]).reshape(3, 1)

    # Compute Epipolar Lines using Fundamental Matrices for both algorithms l' = F * x
    epiline_7 = F_7 @ pt1_hom if F_7 is not None else None
    epiline_8 = F_8 @ pt1_hom if F_8 is not None else None

    xlim, ylim = ax2.get_xlim(), ax2.get_ylim()  # Preserve limits

    ax1.clear()
    ax2.clear()
    ax1.imshow(img1)
    ax2.imshow(img2)  # Keep dimensions unchanged
    ax2.set_xlim(xlim)
    ax2.set_ylim(ylim)

    ax1.scatter(x, y, color="red", marker="x", label="Clicked Point")

    if epiline_7 is not None:
        draw_line(ax2, epiline_7, img2, "b", "7-Point Line")
    if epiline_8 is not None:
        draw_line(ax2, epiline_8, img2, "g", "8-Point Line")

    ax1.set_title("First Image (Click to find Epipolar Lines)")
    ax2.set_title("Second Image with Epipolar Lines")
    fig.canvas.draw()

def draw_line(ax, epiline, img, color, label):
    """Helper function to draw an epipolar line on the given axis."""
    epiline = epiline.flatten()                                         # Flatten epiline to ensure it's one-dimensional
    a, b, c = float(epiline[0]), float(epiline[1]), float(epiline[2])   # Extract coefficients a, b, c from the epipolar line equation
    x1, y1 = 0, int(-c / b) if b != 0 else 0                            # Calculate the first endpoint (x1, y1) of the line
    x2 = img.shape[1]                                                   # Set x2 to the width of the image
    y2 = int((-c - a * x2) / b) if b != 0 else img.shape[0]             # Calculate the second endpoint (x2, y2) of the line
    ax.plot([x1, x2], [y1, y2], color, label=label)                     # Draw the line on the axis from (x1, y1) to (x2, y2) with the specified color
    ax.legend() # Display the legend on the plot

def load_images():
    """Loads images through file dialog and displays them."""
    global img1, img2, fig, ax1, ax2

    # Open file dialogs to select images
    file1 = filedialog.askopenfilename(title="Select First Image")
    file2 = filedialog.askopenfilename(title="Select Second Image")
    if not file1 or not file2:
        print("Image selection cancelled.")
        return

    # Read images in color
    img1 = cv2.imread(file1)
    img2 = cv2.imread(file2)

    # Convert images from BGR to RGB
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

    # Compute fundamental matrices
    compute_fundamental_matrices()

    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    ax1.imshow(img1)
    ax1.set_title("First Image (Click to find Epipolar Lines)")
    ax1.set_axis_off()
    ax2.imshow(img2)  # Keep dimensions unchanged
    ax2.set_title("Second Image")
    ax2.set_axis_off()

    # Connect the click event to the draw_epipolar_lines function
    fig.canvas.mpl_connect("button_press_event", draw_epipolar_lines)
    plt.show()

# GUI for image selection
root = tk.Tk()
root.withdraw()
load_images()
