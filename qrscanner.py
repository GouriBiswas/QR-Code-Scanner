import cv2
import numpy as np  # Import NumPy
from pyzbar.pyzbar import decode

# Open the camera
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Error: Could not access the webcam.")
    exit()

scanned_data = None  # To store scanned QR code data

while True:
    success, frame = cam.read()
    if not success:
        print("Failed to capture image")
        break

    # Decode QR/Barcode
    for barcode in decode(frame):
        scanned_data = barcode.data.decode('utf-8')  # Extract QR code data
        print("Scanned Data:", scanned_data)

        # Draw a rectangle around the detected QR code
        points = barcode.polygon
        if len(points) == 4:
            pts = np.array([(p.x, p.y) for p in points], np.int32)  # Convert to NumPy array
            pts = pts.reshape((-1, 1, 2))  # Reshape for OpenCV
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=3)

        # Show the result for 2 seconds
        cv2.imshow("QR Code Scanner", frame)
        cv2.waitKey(2000)  # Wait for 2 seconds before closing

        # Break the loop once a QR code is scanned
        cam.release()
        cv2.destroyAllWindows()
        print("Camera closed. Returning scanned link...")
        exit(scanned_data)  # Return scanned data

    # Show the camera feed
    cv2.imshow("QR Code Scanner", frame)

    # Exit manually by pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources if no QR is scanned
cam.release()
cv2.destroyAllWindows()

# Return scanned data (if any)
if scanned_data:
    print("Scanned QR Code:", scanned_data)
