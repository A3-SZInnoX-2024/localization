import cv2
import numpy as np

# Load the image
image_path = "/mnt/data/WX20240131-150447@2x.png"
image = cv2.imread(image_path)

# Convert to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define HSV range for each color
# Note: These ranges are estimated, they might need adjustment for precise color detection
color_ranges = {
    "red1": ([0, 100, 100], [10, 255, 255]),
    "red2": ([170, 100, 100], [180, 255, 255]),
    "green": ([35, 100, 100], [85, 255, 255]),
    "blue": ([100, 100, 100], [140, 255, 255]),
    "orange": ([8, 100, 100], [20, 255, 255]),
    "yellow": ([25, 100, 100], [35, 255, 255]),
}


# Function to create mask for each color and find the contours
def identify_color_ranges(image, hsv, color_ranges):
    identified_colors = {}
    for color, (lower, upper) in color_ranges.items():
        # Create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        # Find the colors within the specified boundaries and apply the mask
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)

        # Find contours in the mask
        contours, _ = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        if contours:
            identified_colors[color] = contours

    return identified_colors


# Identify colors
identified_colors = identify_color_ranges(image, hsv, color_ranges)

# Iterate over identified colors and draw contours
for color, contours in identified_colors.items():
    for cnt in contours:
        # Draw a bounding box around the detected object
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Put the color name text on the object
        cv2.putText(
            image, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
        )

# Save the result image
result_path = "/mnt/data/identified_colors.png"
cv2.imwrite(result_path, image)

result_path
