
   Epipolar Geometry Interactive Tool
==========================================


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

``bash
# Optional: create & activate virtualenv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install opencv-python numpy matplotlib
'''\\
## ▶️ Usage

1. **Run the tool**  
   ```bash
   python epipolar_gui.py
Select Images
Two file-picker dialogs will appear—choose your stereo pair.

Click to Visualize
When the Matplotlib window appears, click any point in the first image.

Observe Epipolar Lines
The second image will display:

Blue line from the 7-point algorithm

Green line from the 8-point algorithm


## 📝 Core Functions
compute_fundamental_matrices()
Detects SIFT keypoints, matches via FLANN, computes F_7 & F_8.

draw_epipolar_lines(event)
Handles Matplotlib click events, computes and draws epipolar lines.

load_images()
Uses Tkinter dialogs to select images, sets up the Matplotlib figure, and binds callbacks.

