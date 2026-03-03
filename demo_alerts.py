"""
Quick Demo - Test the Alert System
This script sends test alerts to verify the system is working
"""

import time
from alert_sender import send_accident_alert, send_light_fault_alert, send_collapse_alert

print("=" * 60)
print("  ALERT SYSTEM DEMO")
print("=" * 60)
print()
print("This will send test alerts to the backend.")
print("Make sure:")
print("  1. Backend is running (python backend/ws_server.py)")
print("  2. Frontend is running (cd frontend && npm start)")
print("  3. System user created (email: system@local, password: system123)")
print()
input("Press Enter to start demo...")
print()

# Test 1: Accident Alert
print("📍 Test 1: Sending Accident Alert...")
success1 = send_accident_alert(
    description="Demo: Car collision at intersection",
    location="Camera 1 - Main Street",
    confidence=0.95
)
if success1:
    print("✓ Accident alert sent successfully!")
else:
    print("✗ Failed to send accident alert")
    print("  → Make sure system user exists and backend is running")

time.sleep(2)

# Test 2: Light Fault Alert  
print("\n💡 Test 2: Sending Light Fault Alert...")
success2 = send_light_fault_alert(
    description="Demo: Street light #42 not functioning",
    light_id="Light-042"
)
if success2:
    print("✓ Light fault alert sent successfully!")
else:
    print("✗ Failed to send light fault alert")

time.sleep(2)

# Test 3: Human Collapse Alert
print("\n🚨 Test 3: Sending Human Collapse Alert...")
success3 = send_collapse_alert(
    description="Demo: Person fell and remained on ground",
    location="Sidewalk near Park Avenue"
)
if success3:
    print("✓ Collapse alert sent successfully!")
else:
    print("✗ Failed to send collapse alert")

print()
print("=" * 60)
print("  DEMO COMPLETED")
print("=" * 60)
print()
print("Now check your website:")
print("  → Go to http://localhost:3000")
print("  → Login with your account")
print("  → Click 'Accident Detection' to see the test accident")
print("  → Click 'Light Fault Detection' to see the test fault")
print()
print("The pages auto-refresh every 5 seconds!")
print("=" * 60)
