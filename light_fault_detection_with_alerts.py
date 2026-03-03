"""
Example: Light Fault Detection with Real-time Alerts
This shows how to send light fault alerts to the system
"""

import cv2
import numpy as np
import time
from alert_sender import send_light_fault_alert

cap = cv2.VideoCapture(0)

# Track alerts
last_alert_time = 0
ALERT_COOLDOWN = 30  # Don't send duplicate alerts within 30 seconds

print("💡 Light Fault Detection System Started")
print("✓ Connected to backend - alerts will be sent automatically")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale for brightness analysis
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Calculate average brightness
    avg_brightness = np.mean(gray)
    
    # Simple fault detection: if brightness is too low or too high
    # You can replace this with your actual light fault detection logic
    fault_detected = False
    fault_description = ""
    
    if avg_brightness < 30:  # Too dark - possible light failure
        fault_detected = True
        fault_description = f"Street light possibly OFF - Very low brightness ({avg_brightness:.1f})"
        cv2.putText(frame, "LIGHT FAULT: TOO DARK", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    elif avg_brightness > 200:  # Too bright - possible malfunction
        fault_detected = True
        fault_description = f"Street light malfunction - Excessive brightness ({avg_brightness:.1f})"
        cv2.putText(frame, "LIGHT FAULT: TOO BRIGHT", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
    
    # Display brightness level
    cv2.putText(frame, f"Brightness: {avg_brightness:.1f}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Send alert if fault detected
    if fault_detected:
        current_time = time.time()
        if (current_time - last_alert_time) > ALERT_COOLDOWN:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            description = f"{fault_description} - Detected at {timestamp}"
            
            # Send the alert
            success = send_light_fault_alert(description, light_id="Light-001")
            
            if success:
                cv2.putText(frame, "ALERT SENT TO SYSTEM", (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                print(f"✓ Light fault alert sent at {timestamp}")
                last_alert_time = current_time
            else:
                cv2.putText(frame, "Alert Failed - Check Backend", (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
    
    cv2.imshow("Light Fault Detection with Alerts", frame)
    
    if cv2.waitKey(10) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("System stopped")
