import cv2
import numpy as np

# Open the video file
video_path = 'Test Videos/lbw2.mp4'
video = cv2.VideoCapture(video_path)

# Get video properties
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)

# Create an output video writer
output_path = 'Test Videos/llbw2.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
output_video = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

while video.isOpened():
    # Read a frame from the video
    ret, frame = video.read()

    if not ret:
        break

    # Contrast enhancement
    alpha = 1.5
    beta = 0
    enhanced_frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    # Color enhancement
    hsv = cv2.cvtColor(enhanced_frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = cv2.add(s, 50)
    v = cv2.add(v, 50)
    enhanced_hsv = cv2.merge([h, s, v])
    color_enhanced_frame = cv2.cvtColor(enhanced_hsv, cv2.COLOR_HSV2BGR)

    # Display the processed frame
    cv2.imshow('Output', color_enhanced_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Write the processed frame to the output video
    output_video.write(color_enhanced_frame)

video.release()
output_video.release()
cv2.destroyAllWindows()
