import cv2

video_path = "ScreenRecorderProject1.mp4"
cap = cv2.VideoCapture(video_path)

paused = False
points = []

# Get original video resolution
video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Video", video_width, video_height)  # set to original video size

def mouse(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 2:
        points.append((x, y))
        print("Point:", x, y)

cv2.setMouseCallback("Video", mouse)

while cap.isOpened():
    if not paused:
        ret, frame = cap.read()
        if not ret:
            break

    display = frame.copy()

    # draw rectangle
    if len(points) == 2:
        cv2.rectangle(
            display,
            points[0],
            points[1],
            (0, 255, 0),
            2
        )

        x1, y1 = points[0]
        x2, y2 = points[1]
        print(f"CROP -> x:{x1}, y:{y1}, w:{x2-x1}, h:{y2-y1}")

    cv2.imshow("Video", display)

    key = cv2.waitKey(30)
    if key == 32:  # SPACE
        paused = not paused
    elif key == 27:  # ESC
        break
    elif key == ord('r'):  # reset points
        points = []

cap.release()
cv2.destroyAllWindows()
