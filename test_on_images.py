import tensorflow as tf
import cv2
import os
import numpy as np

# Load trained model
model = tf.keras.models.load_model("accident_cnn_model.h5")

IMG_SIZE = (224, 224)

def predict_image(img_path):
    img = cv2.imread(img_path)

    # SAFETY CHECK
    if img is None:
        return "INVALID_IMAGE", 0.0

    img = cv2.resize(img, IMG_SIZE)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img, verbose=0)[0][0]

    if prediction > 0.5:
        label = "ACCIDENT"
        confidence = prediction
    else:
        label = "NO ACCIDENT"
        confidence = 1 - prediction

    return label, confidence

# Test on some images
test_folders = {
    "accident": "dataset/test/accident",
    "no_accident": "dataset/test/no_accident"
}

for category, folder in test_folders.items():
    print(f"\nTesting {category.upper()} images:")
    images = os.listdir(folder)[:5]   # test first 5 images

    for img_name in images:
        img_path = os.path.join(folder, img_name)
        label, confidence = predict_image(img_path)

if label == "INVALID_IMAGE":
    print(f"{img_name} → skipped (invalid image)")
else:
    print(f"{img_name} → {label} ({confidence*100:.2f}%)")

      
