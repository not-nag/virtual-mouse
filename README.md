# Virtual Mouse with Hand Gestures

This project uses computer vision techniques to create a virtual mouse that tracks hand gestures and translates them into actions on the computer. It allows you to control the cursor movement, left-click, right-click, double-click, drag and drop, and more using hand gestures detected through a webcam.

## Features

- Control cursor movement by placing your index and middle finger together and others fingers curled up.
- Left-click by folding the index finger.
- Right-click by folding the middle finger.
- Double-click by bringing up index, middle and rung finger.
- Raise only pinky finger to keep the mouse press down and Raise only thumb finger to release the mouse press. Used to simulate Drag and Drop functionality.

## Requirements

- Python 3.x
- OpenCV
- MediaPipe
- PyAutoGUI

## How to Run

1. Install the required libraries:

   ```bash
   pip install opencv-python mediapipe pyautogui

2. Clone the repository. Creating a virtual environment is recommended.

   ```bash
   git clone https://github.com/your-username/virtual-mouse.git
   cd virtual-mouse

3. Run the VirtualMouse.py script:

   ```bash
   python VirtualMouse.py
   
  This will open a webcam feed displaying your hand gestures and the virtual mouse interaction.

## Acknowledgements

This project is built using the OpenCV, MediaPipe, and PyAutoGUI libraries. Credits to the developers of these libraries for providing such powerful tools for computer vision and automation.
