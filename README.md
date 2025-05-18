# <!--
==========================================
   Epipolar Geometry Interactive Tool
==========================================
-->

## 🚀 Project Overview  
An interactive Python tool to **automatically compute** the fundamental matrix between two images and **visualize epipolar lines** via both 7-point and 8-point algorithms. Click any point in the first image to overlay:
- **Blue line** (7-point)
- **Green line** (8-point)  
on the second image, illustrating stereo epipolar geometry .

---

## 🎯 Features

- **Dual Fundamental Matrix Estimation**  
  - 7-Point algorithm (exactly 7 correspondences)   
  - 8-Point algorithm (≥8 correspondences)   

- **Robust Feature Matching**  
  - **SIFT** for scale- & rotation-invariant keypoints   
  - **FLANN** for fast descriptor matching   

- **Interactive Visualization**  
  - Matplotlib click events (`mpl_connect`) :contentReference[oaicite:5]{index=5}  
  - Overlays epipolar lines in distinct colors :contentReference[oaicite:6]{index=6}  

- **Cross-Platform GUI**  
  - **Tkinter** file dialogs (`askopenfilename`)   

---

## 🔧 Installation

```bash
# Optional: create & activate virtualenv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install opencv-python numpy matplotlib
%   Usage
%   -----
%   1. Run the tool:
%        python epipolar_gui.py
%
%   2. Select your two stereo images via the file dialogs.
%
%   3. When the Matplotlib window appears, click any point in the first image.
%
%   4. Observe the blue (7-point) and green (8-point) epipolar lines in the second image.
%
%   File Structure
%   --------------
%     epipolar_gui.py      - Main Python script implementing everything
%     requirements.txt     - pip-installable dependency list
%     README.m             - This MATLAB-style comment README
%
%   Core Functions (in epipolar_gui.py)
%   -----------------------------------
%     compute_fundamental_matrices()  - Detects SIFT features, matches them, computes F₇ & F₈
%     draw_epipolar_lines(event)      - Handles clicks, computes & draws epipolar lines
%     load_images()                   - Opens file dialogs, converts BGR→RGB, sets up plot
%
%   Contact & Contributions
%   -----------------------
%   Please open GitHub issues or submit pull requests to propose enhancements,
%   bug fixes, or documentation improvements.
%
% =========================================================================
