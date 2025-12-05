import cv2
import time
import sys
from detector import HandDetector
from utils import calculate_distance, classify_state, draw_virtual_boundary, draw_state_indicator


def main():
    # Initialize hand detector
    detector = HandDetector()
    
    # Open webcam with optimized settings
    cap = cv2.VideoCapture(0)
    
    # Optimize camera settings for performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    # Check if webcam is opened correctly
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    # Set target FPS (increased from 8 to 15 for better performance)
    target_fps = 15
    frame_time = 1.0 / target_fps
    
    prev_time = time.time()
    
    print("Hand Distance Warning System Started")
    print("Press 'q' to quit")
    
    # Test if GUI is available
    gui_available = True
    try:
        # Create a test window to check if GUI is available
        cv2.namedWindow('Test', cv2.WINDOW_AUTOSIZE)
        cv2.destroyWindow('Test')
    except cv2.error:
        gui_available = False
        print("Warning: GUI not available. Running in console mode only.")
        print("Install opencv-python with GUI support for visualization.")
    
    frame_count = 0
    fps_calc_time = time.time()
    
    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read frame from webcam")
            break
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Detect hand
        contour, centroid = detector.detect_hand(frame)
        
        # Draw virtual boundary
        frame, boundary_center, top_left, bottom_right = draw_virtual_boundary(frame)
        
        # Process hand detection results
        if contour is not None and centroid is not None:
            # Draw hand detection
            frame = detector.draw_detection(frame, contour, centroid)
            
            # Calculate distance between hand centroid and boundary center
            distance = calculate_distance(centroid, boundary_center)
            
            # Classify state based on distance
            state = classify_state(distance)
            
            # Draw state indicator
            frame = draw_state_indicator(frame, state, distance)
        else:
            # No hand detected
            state = 'SAFE'
            distance = float('inf')
            frame = draw_state_indicator(frame, state, 0)
        
        # Calculate actual FPS every 30 frames
        frame_count += 1
        if frame_count % 30 == 0:
            current_fps_calc_time = time.time()
            actual_fps = 30 / (current_fps_calc_time - fps_calc_time)
            fps_calc_time = current_fps_calc_time
        else:
            # Use previous FPS calculation if available
            try:
                actual_fps
            except NameError:
                actual_fps = target_fps
        
        # Display FPS on frame
        if gui_available:
            cv2.putText(frame, f'FPS: {actual_fps:.1f}', (10, frame.shape[0] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Display the resulting frame
        if gui_available:
            cv2.imshow('Real-Time Hand Distance Warning System', frame)
            
            # Break loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            # Console mode - print status every 30 frames
            if frame_count % 30 == 0:
                print(f"State: {state}, Distance: {int(distance) if distance != float('inf') else 'N/A'}, FPS: {actual_fps:.1f}")
        
        # FPS control - sleep to maintain target FPS
        current_time = time.time()
        elapsed = current_time - prev_time
        if elapsed < frame_time:
            time.sleep(frame_time - elapsed)
        prev_time = time.time()
    
    # Release webcam and close windows
    cap.release()
    if gui_available:
        cv2.destroyAllWindows()
    print("Hand Distance Warning System Stopped")


if __name__ == "__main__":
    main()