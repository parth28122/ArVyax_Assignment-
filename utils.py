import cv2
import numpy as np


def calculate_distance(point1, point2):
    """
    Calculate Euclidean distance between two points
    
    Args:
        point1: First point (x1, y1)
        point2: Second point (x2, y2)
        
    Returns:
        float: Distance between the two points
    """
    # Using numpy's built-in function for better performance
    return np.linalg.norm(np.array(point1) - np.array(point2))


def classify_state(distance, warning_threshold=150, danger_threshold=50):
    """
    Classify the state based on distance from the virtual boundary
    
    Args:
        distance: Distance between hand centroid and rectangle center
        warning_threshold: Distance threshold for warning state
        danger_threshold: Distance threshold for danger state
        
    Returns:
        str: State classification ('SAFE', 'WARNING', 'DANGER')
    """
    if distance <= danger_threshold:
        return 'DANGER'
    elif distance <= warning_threshold:
        return 'WARNING'
    else:
        return 'SAFE'


def draw_virtual_boundary(frame, boundary_size=(200, 200)):
    """
    Draw a fixed virtual rectangular boundary in the center of the screen
    
    Args:
        frame: Image frame to draw on
        boundary_size: Size of the boundary rectangle (width, height)
        
    Returns:
        tuple: (frame, center_point, top_left, bottom_right)
    """
    height, width = frame.shape[:2]
    
    # Calculate center of the frame
    center_x, center_y = width // 2, height // 2
    
    # Calculate top-left and bottom-right corners of the rectangle
    rect_width, rect_height = boundary_size
    top_left = (center_x - rect_width // 2, center_y - rect_height // 2)
    bottom_right = (center_x + rect_width // 2, center_y + rect_height // 2)
    
    # Draw the rectangle
    cv2.rectangle(frame, top_left, bottom_right, (255, 255, 255), 2)
    
    # Mark the center point
    center_point = (center_x, center_y)
    cv2.circle(frame, center_point, 5, (255, 255, 255), -1)
    
    return frame, center_point, top_left, bottom_right


def draw_state_indicator(frame, state, distance):
    """
    Draw onscreen text overlay for each state
    
    Args:
        frame: Image frame to draw on
        state: Current state ('SAFE', 'WARNING', 'DANGER')
        distance: Distance value to display
        
    Returns:
        frame: Frame with state indicator
    """
    # Define colors for each state
    colors = {
        'SAFE': (0, 255, 0),      # Green
        'WARNING': (0, 255, 255), # Yellow
        'DANGER': (0, 0, 255)     # Red
    }
    
    # Get color for current state
    color = colors.get(state, (255, 255, 255))
    
    # Display state text with reduced font size for better performance
    cv2.putText(frame, f'State: {state}', (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA)
    
    # Display distance with reduced font size for better performance
    cv2.putText(frame, f'Distance: {int(distance)}', (10, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA)
    
    # Special handling for DANGER state - flash "DANGER DANGER"
    if state == 'DANGER':
        # Get frame dimensions
        height, width = frame.shape[:2]
        
        # Draw flashing DANGER text in the center of the frame
        text = "DANGER DANGER"
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
        text_x = (width - text_size[0]) // 2
        text_y = height // 2
        
        cv2.putText(frame, text, (text_x, text_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3, cv2.LINE_AA)
    
    return frame