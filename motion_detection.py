import cv2

# Open camera (0 = laptop webcam, later can be ESP32 stream)
cap = cv2.VideoCapture(0)

# Read first frame
ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    # Difference between frames
    diff = cv2.absdiff(frame1, frame2)

    # Convert to grayscale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Thresholding
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # Dilate to fill gaps
    dilated = cv2.dilate(thresh, None, iterations=3)

    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 800:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.putText(frame1, "Motion Detected", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Motion Detection", frame1)

    frame1 = frame2
    ret, frame2 = cap.read()

    if not ret:
        break

    # Press 'q' to quit
    if cv2.waitKey(40) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
