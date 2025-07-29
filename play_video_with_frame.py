import cv2

cap = cv2.VideoCapture("asl_cut.mp4")
paused = False

while True:
    if not paused:
        ret, frame = cap.read()
        if not ret:
            break

    frame_id = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    display_frame = frame.copy() if frame is not None else None

    if display_frame is not None:
        cv2.putText(display_frame, f"Frame: {frame_id}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Video", display_frame)

    key = cv2.waitKey(30) & 0xFF

    if key == 27:  # ESC để thoát
        break
    elif key == ord(' '):  # Space để pause / resume
        paused = not paused

cap.release()
cv2.destroyAllWindows()
