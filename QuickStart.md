# Quick Start Guide

## Installation Steps

1. **Prerequisites**
   - Python 3.6 or higher installed on your system
   - A working webcam connected to your computer
   - pip package manager (usually comes with Python)

2. **Clone or Download the Repository**
   If you have git installed:
   ```bash
   git clone <repository-url>
   cd hand-distance-tracker
   ```
   
   Or download and extract the project files to a folder.

3. **Install Dependencies**
   Navigate to the project directory and install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
   
   This will install:
   - opencv-contrib-python (for computer vision operations with GUI support)
   - numpy (for numerical computations)

4. **Verify Installation**
   Check that the packages were installed correctly:
   ```bash
   pip show opencv-contrib-python numpy
   ```

## Fast Run Guide

1. **Run the Application**
   Execute the main script to start the hand tracking system:
   ```bash
   python main.py
   ```

2. **Using the Application**
   - Position your hand in front of the webcam
   - The system will detect your hand and track its movement
   - A white rectangular boundary will appear in the center of the screen
   - Watch the state indicator at the top left of the screen:
     - **GREEN "SAFE"**: Your hand is far from the boundary
     - **YELLOW "WARNING"**: Your hand is approaching the boundary
     - **RED "DANGER"**: Your hand is touching or inside the boundary
   - During DANGER state, the screen will flash "DANGER DANGER" in bright red

3. **Exit the Application**
   Press the 'q' key to stop the application and close the window.

## Troubleshooting

### Common Issues and Solutions

1. **"Error: Could not open webcam"**
   - Make sure your webcam is properly connected
   - Check that no other application is using the webcam
   - Try restarting your computer
   - On Windows, check camera privacy settings

2. **No hand detection or poor detection**
   - Ensure good lighting conditions
   - Position your hand against a contrasting background
   - Adjust your distance from the camera (about arm's length works best)
   - Make sure your hand is fully visible in the frame

3. **"ModuleNotFoundError" when running python main.py**
   - Make sure you've installed the dependencies with `pip install -r requirements.txt`
   - Check that you're running the command from the project directory
   - Verify your Python environment

4. **Low FPS or laggy performance**
   - Close other applications to free up CPU resources
   - Ensure your system meets the minimum requirements
   - The system is optimized for 15+ FPS on modern CPUs
   - If still experiencing low FPS, try reducing the camera resolution in main.py

5. **Incorrect skin detection**
   - The HSV thresholds are tuned for typical skin tones
   - Different lighting conditions may affect detection
   - The system works best with natural skin tones against non-skin colored backgrounds

6. **GUI Window Not Appearing (OpenCV Error)**
   - This happens when opencv-python is installed without GUI support
   - The program will automatically fall back to console mode
   - To enable GUI visualization, install opencv-contrib-python:
     ```bash
     pip uninstall opencv-python
     pip install opencv-contrib-python
     ```
   - Alternatively, you can use the console output which displays state information periodically

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.12+, or Linux
- **Python Version**: 3.6 or higher
- **RAM**: Minimum 4GB recommended
- **CPU**: Modern processor with at least 2 cores
- **Webcam**: Any standard USB webcam

### Performance Tuning

The application is optimized to run at 15+ FPS on CPU-only systems. If you're experiencing performance issues:

1. **Adjust Camera Resolution**
   - In `main.py`, modify the camera resolution settings:
     ```python
     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # Try 320 for lower resolution
     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Try 240 for lower resolution
     ```

2. **Modify FPS Target**
   - Change the target FPS in `main.py`:
     ```python
     target_fps = 15  # Lower this value if needed
     ```

### Fine-tuning Tips

1. **Adjusting Skin Detection Sensitivity**
   - Modify the HSV range values in `detector.py`:
     ```python
     self.lower_skin = np.array([0, 20, 70], dtype=np.uint8)
     self.upper_skin = np.array([20, 255, 255], dtype=np.uint8)
     ```
   - Lower values in lower_skin make detection more sensitive
   - Higher values in upper_skin include more colors

2. **Changing Distance Thresholds**
   - Modify the thresholds in `utils.py`:
     ```python
     def classify_state(distance, warning_threshold=150, danger_threshold=50):
     ```
   - Increase thresholds for larger safety margins
   - Decrease thresholds for more sensitive detection

### Support

If you continue to experience issues not covered in this guide, please:
1. Check that all dependencies are correctly installed
2. Ensure your Python environment is properly configured
3. Verify your webcam is functioning in other applications
4. Consult the OpenCV documentation for platform-specific webcam issues

For bugs or feature requests, please submit an issue to the project repository.