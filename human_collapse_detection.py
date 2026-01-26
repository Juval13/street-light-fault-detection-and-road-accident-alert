import cv2
import time
from mediapipe import Image, ImageFormat
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# =========================
# LOAD POSE MODEL
# =========================
MODEL_PATH = "pose_landmarker_lite.task"

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_poses=1
)

pose_landmarker = vision.PoseLandmarker.create_from_options(options)

# =========================
# CAMERA SETUP
# =========================
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not accessible")
    exit()

print("🧍 Human Collapse Detection Started (press 'q' to quit)")

# =========================
# STATE VARIABLES
# =========================
fall_start_time = None
FALL_CONFIRM_TIME = 2      # seconds
DISPLAY_DURATION = 10      # seconds

last_alert_time = 0
last_alert_text = "Monitoring..."
last_alert_color = (0, 255, 0)

frame_timestamp = 0

# =========================
# MAIN LOOP
# =========================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = Image(
        image_format=ImageFormat.SRGB,
        data=rgb
    )

    result = pose_landmarker.detect_for_video(
        mp_image,
        frame_timestamp
    )
    frame_timestamp += 1

    fall_detected = False
    lying_down = False

    if result.pose_landmarks:
        lm = result.pose_landmarks[0]

        # Nose = 0, Left ankle = 28
        head_y = lm[0].y
        ankle_y = lm[28].y

        body_height = abs(head_y - ankle_y)

        # -------------------------
        # LYING-DOWN DETECTION
        # -------------------------
        if body_height < 0.15:
            lying_down = True
            fall_detected = True

        # Draw pose points
        for point in lm:
            cx, cy = int(point.x * w), int(point.y * h)
            cv2.circle(frame, (cx, cy), 3, (255, 0, 0), -1)

    # =========================
    # TEMPORAL CONFIRMATION
    # =========================
    if fall_detected:
        if fall_start_time is None:
            fall_start_time = time.time()
        elif time.time() - fall_start_time >= FALL_CONFIRM_TIME:
            last_alert_time = time.time()
            last_alert_text = "🚨 HUMAN COLLAPSE DETECTED"
            last_alert_color = (0, 0, 255)
    else:
        fall_start_time = None

    # =========================
    # ALERT DISPLAY (10s latch)
    # =========================
    if time.time() - last_alert_time < DISPLAY_DURATION:
        display_text = last_alert_text
        display_color = last_alert_color
    else:
        display_text = "Monitoring..."
        display_color = (0, 255, 0)

    cv2.putText(
        frame,
        display_text,
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        display_color,
        2
    )

    posture = "LYING" if lying_down else "STANDING"
    posture_color = (0, 0, 255) if lying_down else (0, 255, 0)

    cv2.putText(
        frame,
        f"Posture: {posture}",
        (10, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        posture_color,
        2
    )

    cv2.imshow("Human Collapse Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# =========================
# CLEANUP
# =========================
cap.release()
cv2.destroyAllWindows()
pose_landmarker.close()
print("System stopped.")
