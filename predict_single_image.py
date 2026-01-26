import tensorflow as tf
import cv2
import numpy as np

# =========================
# CONFIGURATION
# =========================
MODEL_PATH = "accident_cnn_model.h5"
IMG_SIZE = (224, 224)
CONFIDENCE_THRESHOLD = 0.80  # 80%

# =========================
# LOAD MODEL
# =========================
model = tf.keras.models.load_model(MODEL_PATH)

# =========================
# SIMULATED MOTION FUNCTIONS
# (single image cannot measure motion)
# =========================
def motion_detected_simulated():
    return True

def sudden_motion_simulated():
    return True

# =========================
# PREDICTION FUNCTION
# =========================
def predict_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        print("❌ Invalid image path or unreadable image")
        return

    # Preprocess
    img = cv2.resize(img, IMG_SIZE)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    # CNN prediction
    prediction = model.predict(img, verbose=0)[0][0]

    if prediction > 0.5:
        cnn_label = "ACCIDENT"
        cnn_confidence = prediction
    else:
        cnn_label = "NO ACCIDENT"
        cnn_confidence = 1 - prediction

    # Simulated motion flags
    motion_detected = motion_detected_simulated()
    sudden_motion = sudden_motion_simulated()

    # =========================
    # CORRECT HYBRID LOGIC
    # =========================
    if (
        motion_detected
        and sudden_motion
        and cnn_label == "ACCIDENT"
        and cnn_confidence >= CONFIDENCE_THRESHOLD
    ):
        final_decision = "🚨 ACCIDENT ALERT"
    else:
        final_decision = "✅ IGNORE / NO ACCIDENT"

    # =========================
    # OUTPUT
    # =========================
    print("\n----- Prediction Result -----")
    print(f"CNN Output        : {cnn_label}")
    print(f"CNN Confidence    : {cnn_confidence*100:.2f}%")
    print(f"Motion Detected   : {motion_detected}")
    print(f"Sudden Motion     : {sudden_motion}")
    print(f"Final Decision    : {final_decision}")
    print("-----------------------------\n")

# =========================
# INPUT IMAGE PATH
# =========================
predict_image("C:/Users/soura/Downloads/pic2.jpeg")
