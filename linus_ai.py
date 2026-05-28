import cv2
from edge_impulse_linux.image import ImageImpulseRunner

model_path = "/home/linus/lab_attire/model.eim"

def main():
    runner = ImageImpulseRunner(model_path)
    model_info = runner.init()
    labels = model_info['model_parameters']['labels']
    print("Model initialized successfully!")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open camera. Check usbipd setup.")
        return

    print("Camera active. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process for AI
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        features, cropped = runner.get_features_from_image(img)
        res = runner.classify(features)

        # Draw bounding boxes on frame
        if "bounding_boxes" in res["result"]:
            for bb in res["result"]["bounding_boxes"]:
                if bb["value"] > 0.5:  # Only show if confidence > 50%
                    x = int(bb["x"] * frame.shape[1] / cropped.shape[1])
                    y = int(bb["y"] * frame.shape[0] / cropped.shape[0])
                    w = int(bb["width"] * frame.shape[1] / cropped.shape[1])
                    h = int(bb["height"] * frame.shape[0] / cropped.shape[0])

                    # Draw rectangle
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Draw label and confidence
                    label = f'{bb["label"]} {bb["value"]:.0%}'
                    cv2.putText(frame, label, (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Display the frame with boxes
        cv2.imshow('Lab Attire Scanner', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    runner.stop()

if __name__ == "__main__":
    main()