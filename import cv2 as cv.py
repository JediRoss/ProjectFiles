import cv2
import numpy as np

def get_center_region(frame, region_size):
    height, width, _ = frame.shape
    start_x = width // 2 - region_size // 2
    start_y = height // 2 - region_size // 2
    end_x = start_x + region_size
    end_y = start_y + region_size
    
    return frame[start_y:end_y, start_x:end_x]

def calculate_average_color(region):
    avg_color_per_row = np.average(region, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    return avg_color

# Open a connection to the default camera (usually the first camera, index 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

region_size = 100  # Size of the region to be averaged

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read frame.")
        break

    # Get the center region of the frame
    center_region = get_center_region(frame, region_size)
    
    # Calculate the average color of the center region
    avg_color = calculate_average_color(center_region)
    avg_color_int = tuple(map(int, avg_color))  # Convert to integer for display
    
    # Display the center region with a rectangle
    height, width, _ = frame.shape
    start_x = width // 2 - region_size // 2
    start_y = height // 2 - region_size // 2
    end_x = start_x + region_size
    end_y = start_y + region_size
    cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
    
    # Show the average color in the window
    cv2.putText(frame, f'Avg Color: {avg_color_int}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Display the resulting frame
    cv2.imshow('Camera Feed', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()