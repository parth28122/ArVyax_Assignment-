# Real-Time Hand Distance Warning System

## Project Overview

This project implements a real-time hand tracking and distance warning system using classical computer vision techniques with OpenCV. The system uses a webcam feed to detect the user's hand through HSV skin color segmentation, tracks the hand position, and provides visual warnings based on the proximity of the hand to a virtual boundary in the center of the screen.

The system classifies the hand's proximity into three states:
- **SAFE**: Hand is far from the boundary
- **WARNING**: Hand is approaching the boundary
- **DANGER**: Hand is touching or inside the boundary

During the DANGER state, the screen flashes "DANGER DANGER" in bright red to alert the user.

## Features

- Real-time hand detection using HSV skin color thresholding
- Hand centroid calculation via image moments
- Fixed virtual rectangular boundary in the center of the screen
- Distance measurement between hand centroid and boundary center
- Three-state classification system (SAFE, WARNING, DANGER)
- Visual indicators for each state
- Bright red "DANGER DANGER" flash during danger state
- Graceful fallback to console mode if GUI is not available
- Optimized for performance - maintains 15+ FPS on CPU-only systems

## Technologies Used

- Python 3.x
- OpenCV (cv2) with GUI support
- NumPy

## Project Structure

```
hand-distance-tracker/
├── main.py              # Main application entry point
├── detector.py          # Hand detection logic using HSV segmentation
├── utils.py             # Utility functions for distance calculation and visualization
├── requirements.txt     # Python package dependencies
├── README.md            # Project documentation
└── QuickStart.md        # Installation and quick start guide
```

## How It Works

1. **Hand Detection**: The system captures video from the webcam and converts each frame to HSV color space. It then applies a skin color threshold to isolate the hand region.

2. **Contour Analysis**: The largest contour in the segmented image is assumed to be the hand. The centroid of this contour is calculated using image moments.

3. **Virtual Boundary**: A fixed rectangular boundary is drawn in the center of the screen.

4. **Distance Calculation**: The Euclidean distance between the hand centroid and the center of the virtual boundary is computed.

5. **State Classification**: Based on the distance, the system classifies the state as SAFE, WARNING, or DANGER.

6. **Visual Feedback**: On-screen indicators show the current state and distance. During DANGER state, the screen flashes "DANGER DANGER".

## Running the Application

To run the application, follow these steps:

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the main script:
   ```bash
   python main.py
   ```

3. To exit the application, press the 'q' key.

For detailed installation instructions and troubleshooting, please refer to [QuickStart.md](QuickStart.md).

## Performance

The system is optimized to run at 15+ FPS on CPU-only systems using only OpenCV and NumPy, without any specialized hardware acceleration or cloud services. Performance optimizations include:

- Frame resizing for faster processing
- Optimized morphological operations
- Efficient distance calculations
- Reduced rendering overhead

## GUI Support

The application automatically detects if GUI support is available. If not, it gracefully falls back to console mode with periodic status updates. For full visualization, make sure to install the opencv-contrib-python package as specified in requirements.txt.

## License

This project is open-source and available under the MIT License.