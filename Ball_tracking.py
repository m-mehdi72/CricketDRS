import cv2
import numpy as np
from cvzone.ColorModule import ColorFinder
from scipy.interpolate import UnivariateSpline
from cvzone.Utils import findContours

# Creating colorfinder objects
myColorFinder = ColorFinder(False)
hsvVals = {'hmin': 170, 'smin': 199, 'vmin': 235, 'hmax': 179, 'smax': 255, 'vmax': 255}

# Declaring variables
posList = []

cap = cv2.VideoCapture('Test Videos/lbw2.mp4')
paused = False
last_frame = None

while True:
    if not paused:
        success, img = cap.read()
        if not success:
            break

    # img = cv2.imread('Ball6.png')
    # Finding ball color
    imgColor, mask = myColorFinder.update(img, hsvVals)

    # Ball Location
    imgContours, contours = findContours(img, mask, minArea=0.2)

    if contours:
        posList.append(contours[0]['center'])

    

    # imgContours = cv2.resize(imgContours, (0, 0), None, 0.5, 0.5)
    cv2.imshow("IMG COLOR", cv2.resize(imgColor, (0, 0), None, 0.5, 0.5))
    cv2.waitKey(20)

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1:
        last_frame = img.copy()

    if cv2.waitKey(1) & 0xFF == ord(' '):
        paused = not paused

cap.release()
cv2.destroyAllWindows()

# # Display the last frame separately
# if last_frame is not None:
#     for i, pos in enumerate(posList):
#         cv2.imshow('Last Frame', last_frame)
#         cv2.waitKey(50)
#         cv2.circle(last_frame, (pos), 15, (0, 0, 255), cv2.FILLED)
#         if i == 0:
#             cv2.line(last_frame, pos, pos, (0, 0, 255), 30)
#         else:
#             cv2.line(last_frame, pos, posList[i - 1], (0, 0, 255), 30)
    
# graph_image = cv2.resize(last_frame, (0, 0), None, 0.7, 0.7)
# height, width = graph_image.shape[:2]

# Create a copy of the last_frame image
graph_image = last_frame.copy()

# Find the last and second-last points in posList
last_point = posList[-1]
second_last_point = posList[-2]

# Calculate the direction vector from the second-last point to the last point
direction_vector = np.array(last_point) - np.array(second_last_point)

# Define the length of the blue line extension
blue_line_extension = 5

# Calculate the endpoint of the blue line by extending from the last point
blue_line_endpoint = last_point + blue_line_extension * direction_vector

# Get the dimensions of the last_frame image
image_height, image_width, _ = graph_image.shape

# Create a window to display the lines on the last frame
cv2.namedWindow('Lines on Last Frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Lines on Last Frame', int(image_width * 0.5), int(image_height * 0.5))

# Draw the lines between consecutive points in posList in red
for i in range(len(posList) - 1):
    cv2.line(graph_image, posList[i], posList[i + 1], (0, 0, 255), 30)
    cv2.imshow('Lines on Last Frame', cv2.resize(graph_image, (0, 0), None, 0.5, 0.5))
    cv2.waitKey(20)

# Draw the blue line
cv2.line(graph_image, last_point, tuple(blue_line_endpoint), (255, 0, 0), 30)
cv2.imshow('Lines on Last Frame', cv2.resize(graph_image, (0, 0), None, 0.5, 0.5))
cv2.waitKey(0)

cv2.destroyAllWindows()


# import cv2
# import numpy as np
# from cvzone.ColorModule import ColorFinder
# from scipy.interpolate import UnivariateSpline
# from cvzone.Utils import findContours

# # Creating colorfinder object
# myColorFinder = ColorFinder(False) 
# hsvVals = {'hmin': 152, 'smin': 157, 'vmin': 192, 'hmax': 179, 'smax': 255, 'vmax': 255}

# # Declaring variables
# posList = []

# def read_video_file(file_path):
#     """Reads the video file and returns the video capture object."""
#     cap = cv2.VideoCapture(file_path)
#     return cap

# def detect_ball_position(frame):
#     """Detects the ball position in the given frame."""
#     imgColor, mask = myColorFinder.update(frame, hsvVals)
#     imgContours, contours = findContours(frame, mask, minArea=0.5)

#     if contours:
#         posList.append(contours[0]['center'])

#     return imgContours


# def visualize_trajectory(last_frame, posList, prediction_distance=50):
#     """Visualizes the ball trajectory on the last frame."""
#     graph_image = last_frame.copy()

#     for i in range(len(posList) - 1):
#         cv2.line(graph_image, posList[i], posList[i + 1], (0, 0, 255), 20)

#     # Calculate spline for smoother trajectory
#     sorted_posList = sorted(posList, key=lambda pos: pos[0])
#     x, y = zip(*sorted_posList)

#     # Remove NaN values from the data
#     valid_indices = np.logical_not(np.isnan(x))
#     x = np.array(x)[valid_indices]
#     y = np.array(y)[valid_indices]

#     spl = UnivariateSpline(x, y)

#     # Generate smoothed positions using the spline function
#     smoothed_positions = [(int(x_val), int(spl(x_val))) for x_val in np.linspace(x[0], x[-1], len(x) * 10) if not np.isnan(spl(x_val))]

#     # Draw the smoothed trajectory
#     for i in range(len(smoothed_positions) - 1):
#         cv2.line(graph_image, smoothed_positions[i], smoothed_positions[i + 1], (0, 255, 0), 5)

#     # Predict the future position based on the last known position
#     last_known_position = posList[-1]
#     prediction_x = last_known_position[0] + prediction_distance

#     # Check if prediction_x is within the range of available positions
#     if prediction_x >= x[0] and prediction_x <= x[-1]:
#         predicted_position = (int(prediction_x), int(spl(prediction_x)))
#         cv2.line(graph_image, last_known_position, predicted_position, (255, 0, 0), 5)

#     # Display the last frame with the trajectory and prediction line
#     cv2.imshow('Lines on Last Frame', cv2.resize(graph_image, (0, 0), None, 0.5, 0.5))
#     cv2.waitKey(0)


# def main():
#     cap = read_video_file('output1.mp4')
#     paused = False
#     last_frame = None

#     while True:
#         if not paused:
#             success, frame = cap.read()
#             if not success:
#                 print("Error reading video file.")
#                 break

#         imgContours = detect_ball_position(frame)

#         imgContours = cv2.resize(imgContours, (0, 0), None, 0.5, 0.5)
#         cv2.imshow("IMG COLOR", cv2.resize(frame, (0, 0), None, 0.5, 0.5))
#         cv2.waitKey(20)

#         if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1:
#             last_frame = frame.copy()

#         if cv2.waitKey(1) & 0xFF == ord(' '):
#             paused = not paused

#     cap.release()
#     cv2.destroyAllWindows()

#     if last_frame is not None:
#         visualize_trajectory(last_frame, posList)

# if __name__ == '__main__':
#     main()
