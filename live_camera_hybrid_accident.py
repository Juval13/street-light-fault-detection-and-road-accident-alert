import cv2
import numpy as np
import tensorflow as tf
import time

from mediapipe import Image, ImageFormat
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# =========================
# CONFIGURATION
# =========================
IMG_SIZE = (224, 224)
CONF_THRESHOLD = 0.80

MOTION_THRESHOLD = 5000
SUDDEN_MOTION_THRESHOLD = 15000

FALL_CONFIRM_TIME = 2          # seconds
DISPLAY_DURATION = 10          # seconds

# =========================
# LOAD MODELS
# =========================
cnn_model = tf.keras.models.load_model("accident_cnn_model.h5")

base_options = python.BaseOptions(
    model_asset_path="pose_landmarker_lite.task"
)
pose_options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_poses=1
)
pose_landmarker = vision.PoseLandmarker.create_from_options(pose_options)

# =========================
# CAMERA SETUP
# =========================
cap = cv2.VideoCapture(0)
ret, prev_frame = cap.read()

if not ret:
    print("❌ Camera not accessible")
    exit()

prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

print("🚦 Smart Street Safety System Started (press 'q' to quit)")

# =========================
# ALERT STATE (CRITICAL FIX)
# =========================
alert_active = False
alert_type = None          # "ACCIDENT" or "FALL"
alert_start_time = 0

# Human fall timing
fall_start_time = None

frame_timestamp = 0

# =========================
# MAIN LOOP
# =========================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # =========================
    # MOTION DETECTION
    # =========================
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    diff = cv2.absdiff(prev_gray, gray)
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    motion_area = np.sum(thresh)
    motion_detected = motion_area > MOTION_THRESHOLD
    sudden_motion = motion_area > SUDDEN_MOTION_THRESHOLD

    prev_gray = gray

    # =========================
    # ROAD ACCIDENT DETECTION
    # =========================
    if motion_detected and sudden_motion and not alert_active:
        img = cv2.resize(frame, IMG_SIZE) / 255.0
        img = np.expand_dims(img, axis=0)

        pred = cnn_model.predict(img, verbose=0)[0][0]

        if pred > 0.5:
            label = "ACCIDENT"
            confidence = pred
        else:
            label = "NO ACCIDENT"
            confidence = 1 - pred

        if label == "ACCIDENT" and confidence >= CONF_THRESHOLD:
            alert_active = True
            alert_type = "ACCIDENT"
            alert_start_time = time.time()

        cv2.putText(
            frame,
            f"CNN: {label} ({confidence*100:.1f}%)",
            (10, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            2
        )

    # =========================
    # HUMAN COLLAPSE DETECTION
    # =========================
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

    lying_down = False

    if result.pose_landmarks:
        lm = result.pose_landmarks[0]

        head_y = lm[0].y
        ankle_y = lm[28].y

        body_height = abs(head_y - ankle_y)

        if body_height < 0.15:
            lying_down = True

        # Draw pose points
        h, w, _ = frame.shape
        for p in lm:
            cv2.circle(
                frame,
                (int(p.x * w), int(p.y * h)),
                3,
                (255, 0, 0),
                -1
            )

    # Temporal confirmation for fall
    if lying_down:
        if fall_start_time is None:
            fall_start_time = time.time()
        elif time.time() - fall_start_time >= FALL_CONFIRM_TIME:
            # Human collapse has PRIORITY
            alert_active = True
            alert_type = "FALL"
            alert_start_time = time.time()
    else:
        fall_start_time = None

    # =========================
    # ALERT DISPLAY (FIXED 10s LATCH)
    # =========================
    if alert_active:
        elapsed = time.time() - alert_start_time

        if elapsed < DISPLAY_DURATION:
            if alert_type == "FALL":
                text = "🚨 HUMAN COLLAPSE DETECTED"
            else:
                text = "🚨 ROAD ACCIDENT DETECTED"
            color = (0, 0, 255)
        else:
            alert_active = False
            alert_type = None
            text = "Monitoring..."
            color = (0, 255, 0)
    else:
        text = "Monitoring..."
        color = (0, 255, 0)

    cv2.putText(
        frame,
        text,
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        color,
        2
    )

    posture = "LYING" if lying_down else "STANDING"
    cv2.putText(
        frame,
        f"Posture: {posture}",
        (10, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255) if lying_down else (0, 255, 0),
        2
    )

    cv2.imshow("Smart Street Safety System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# =========================
# CLEANUP
# =========================
cap.release()
cv2.destroyAllWindows()
pose_landmarker.close()
print("System stopped.")
