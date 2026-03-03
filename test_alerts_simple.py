"""
Simple Alert Test - No user input required
"""

import time
from alert_sender import send_accident_alert, send_light_fault_alert

print("🚀 Testing Alert System...")
print()

# First, need to register system user if not exists
print("Step 1: Make sure system user exists")
print("  → Go to http://localhost:3000/register")
print("  → Create user: email=system@local, password=system123, phone=1234567890")
print()

time.sleep(1)

# Test accident alert
print("Sending test accident alert...")
result1 = send_accident_alert(
    "Test: Vehicle collision detected",
    location="Main Street Camera",
    confidence=0.92
)

time.sleep(2)

# Test light fault
print("Sending test light fault alert...")
result2 = send_light_fault_alert(
    "Test: Street light malfunction detected",
    light_id="SL-123"
)

print()
if result1 or result2:
    print("✅ SUCCESS! Check your website at http://localhost:3000")
    print("   → Login and go to 'Accident Detection' or 'Light Fault Detection'")
else:
    print("⚠️  Please create system user first:")
    print("   → Email: system@local")
    print("   → Password: system123")
