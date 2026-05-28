import cv2

# Open your laptop's standard webcam (0).
# Tomorrow, MF handles the hardware camera connection, not you!
cap = cv2.VideoCapture(0)


def get_processed_frame():
    """
    This is the magic function your GUI will call 60 times a second.
    It returns 3 things: The image, the text to display, and the background color.
    """
    ret, frame = cap.read()

    if not ret:
        return None, "Camera Error", "red"

    # --- FAKE AI PROCESSING ---
    # We are drawing a fake green bounding box to simulate Farid's YOLOv8
    cv2.rectangle(frame, (150, 100), (450, 400), (0, 255, 0), 3)
    cv2.putText(frame, "AI DETECTION: Proper Attire", (160, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    status_text = "Proper Attire - Door Unlocked"
    status_color = "green"

    # Send the finished frame and text back to Izz's GUI
    return frame, status_text, status_color