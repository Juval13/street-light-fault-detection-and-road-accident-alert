import cv2
import time

cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

motion_counter = 0
no_motion_start = None
ACCIDENT_DELAY = 3   # seconds of no motion after big motion

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    large_motion = False

    for contour in contours:
        if cv2.contourArea(contour) > 1500:
            large_motion = True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Detect sudden large motion
    if large_motion:
        motion_counter += 1
        no_motion_start = None
        cv2.putText(frame1, "Large Motion Detected", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # After motion, check for no motion
    else:
        if motion_counter > 10:
            if no_motion_start is None:
                no_motion_start = time.time()
            elif time.time() - no_motion_start > ACCIDENT_DELAY:
                cv2.putText(frame1, "ACCIDENT DETECTED", (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.imshow("Accident Detection", frame1)

    frame1 = frame2
    ret, frame2 = cap.read()
    if not ret:
        break

    if cv2.waitKey(40) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
